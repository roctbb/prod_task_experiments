from .alchemy import *


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String())
    countryCode = db.Column(db.String(2))
    isPublic = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(20), unique=True)
    image = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tokens = db.relationship('ApiToken', backref=backref('user', uselist=False), lazy=True)

    def as_dict(self):
        description = {
            "login": self.login,
            "email": self.email,
            "countryCode": self.countryCode,
            "isPublic": self.isPublic,
        }

        if self.phone:
            description['phone'] = self.phone

        if self.image:
            description['phone'] = self.image

        return description
