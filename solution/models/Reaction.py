from .alchemy import *


class Reaction(db.Model):
    __tablename__ = 'reactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    emotion = db.Column(db.String(10), default='like', index=True)