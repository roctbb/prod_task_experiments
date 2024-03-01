from .alchemy import *
from sqlalchemy.dialects.postgresql import JSON


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text)
    tags = db.Column(JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = db.relationship('User')
    reactions = db.relationship('Reaction', lazy=False)

    def as_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "tags": self.tags,
            "author": self.author.login,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "likesCount": len(list(filter(lambda r: r.reaction == "like", self.reactions))),
            "dislikesCount": len(list(filter(lambda r: r.reaction == "like", self.reactions)))
        }
