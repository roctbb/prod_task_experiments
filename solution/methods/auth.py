from datetime import datetime

import bcrypt
from flask import request
from models import User, db, ApiToken
from helpers import transaction
from exceptions import *
import secrets


@transaction
def create_user(query):
    login_user = User.query.filter(
        (User.login == query.login) | (User.email == query.email)).first()
    phone_user = User.query.filter(User.phone == query.phone).first()

    if login_user or phone_user:
        raise NotUnique

    password_hash = bcrypt.hashpw(query.password.encode(), bcrypt.gensalt())
    user = User(login=query.login, email=query.email, password=password_hash.decode(),
                countryCode=query.countryCode,
                isPublic=query.isPublic, phone=query.phone, image=query.image)
    db.session.add(user)

    return user


@transaction
def patch_user(user, query):
    if query.phone and query.phone != user.phone and User.query.filter(User.phone == query.phone).first():
        raise NotUnique

    if query.isPublic != None:
        user.isPublic = query.isPublic
    if query.countryCode != None:
        user.countryCode = query.countryCode
    if query.phone != None:
        user.phone = query.phone
    if query.image != None:
        user.image = query.image

    return user


@transaction
def authorize_user(login, password):
    user = User.query.filter_by(login=login).first()

    if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
        raise IncorrectAuth

    token = ApiToken(user_id=user.id, token=secrets.token_hex(32))
    db.session.add(token)

    return token


@transaction
def change_user_password(user, old_password, password):
    if not bcrypt.checkpw(old_password.encode(), user.password.encode()):
        raise AccessDenied

    user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    ApiToken.query.filter_by(user_id=user.id).update({ApiToken.expires_at: datetime.utcnow()})


def find_user_by_token(token):
    token = ApiToken.query.filter_by(token=token).filter(ApiToken.expires_at > datetime.utcnow()).first()

    if not token:
        raise IncorrectAuth

    return token.user


def find_public_profile(login):
    user = User.query.filter_by(login=login).first()

    if not user or not user.isPublic:
        raise AccessDenied

    return user


def get_bearer_token():
    auth_header = request.headers.get('Authorization', None)

    if auth_header:
        parts = auth_header.split()
        if parts[0].lower() == 'bearer' and len(parts) == 2:
            return parts[1]

    raise IncorrectAuth


def requires_auth(func):
    def wrapper(*args, **kwargs):
        token = get_bearer_token()
        user = find_user_by_token(token)
        return func(user, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
