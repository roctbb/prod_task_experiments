from datetime import datetime

import bcrypt
from flask import request

from methods.friends import is_friends
from models import db, Post, Reaction
from helpers import transaction
from werkzeug.exceptions import NotFound
from exceptions import *
import secrets


@transaction
def add_post_from_user(user, query):
    post = Post(author_id=user.id, content=query.content, tags=query.tags)
    db.session.add(post)

    return post


def find_post_by_id(post_id):
    return Post.query.filter_by(id=post_id).first_or_404()


def get_posts_for_user(user, pagination=None):
    if pagination:
        posts = Post.query.filter_by(author_id=user.id).order_by(Post.created_at.desc()).limit(pagination.limit).offset(
            pagination.offset)
    else:
        posts = Post.query.filter_by(author_id=user.id).order_by(Post.created_at.desc())

    return posts.all()


@transaction
def set_reaction(post, user, emotion):
    reaction = Reaction.query.filter_by(post_id=post.id, user_id=user.id).first()

    if reaction:
        reaction.emotion = emotion
    else:
        reaction = Reaction(post_id=post.id, user_id=user.id, emotion=emotion)
        db.session.add(reaction)


def has_access_to_feed(user, author):
    if author.isPublic or author.id == user.id or is_friends(user, author):
        return True
    return False
