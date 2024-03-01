from .alchemy import *


class Friend(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id],
                           backref=db.backref('friends', order_by="Friend.added_at.desc()"))
    friend = db.relationship('User', foreign_keys=[friend_id],
                             backref=db.backref('subscriptions', order_by="Friend.added_at.desc()"))

    def as_dict(self):
        return {
            "login": self.friend.login,
            "addedAt": self.added_at.isoformat(timespec="seconds")
        }