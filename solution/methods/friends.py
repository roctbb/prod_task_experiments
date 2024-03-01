from datetime import datetime

import bcrypt
from flask import request
from models import User, db, ApiToken, Friend
from helpers import transaction
from exceptions import *
import secrets


@transaction
def add_to_friends(user, friend):
    if not Friend.query.filter_by(user_id=user.id, friend_id=friend.id).first():
        db.session.add(Friend(user_id=user.id, friend_id=friend.id))


@transaction
def remove_from_friends(user, friend):
    record = Friend.query.filter_by(user_id=user.id, friend_id=friend.id).first()

    if record:
        db.session.delete(record)


def get_user_friends(user, pagination=None):
    if pagination:
        friends = Friend.query.filter_by(user_id=user.id).order_by(Friend.added_at.desc()).limit(
            pagination.limit).offset(pagination.offset)
    else:
        friends = Friend.query.filter_by(user_id=user.id).order_by(Friend.added_at.desc())

    return friends.all()


def is_friends(user, friend):
    return Friend.query.filter_by(user_id=friend.id, friend_id=user.id).first() != None
