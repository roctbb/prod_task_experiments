from datetime import datetime

import bcrypt
from flask import request
from models import db, Post
from helpers import transaction
from exceptions import *
import secrets


@transaction
def add_post_from_user(user, query):
    post = Post(author_id=user.id, content=query.content, tags=query.tags)
    db.session.add(post)

    return post