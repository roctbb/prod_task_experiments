from .alchemy import *
from .User import User

class ApiToken(db.Model):
    __tablename__ = 'api_token'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"))
    token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24))

    def as_dict(self):
        return {
            "token": self.token,
        }