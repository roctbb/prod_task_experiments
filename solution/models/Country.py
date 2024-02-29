from .alchemy import *

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    alpha2 = db.Column(db.String(2), nullable=False)
    alpha3 = db.Column(db.String(3), nullable=False)
    region = db.Column(db.String(100), nullable=False)

    def as_dict(self):
        return {
            "name": self.name,
            "alpha2": self.alpha2,
            "alpha3": self.alpha3,
            "region": self.region
        }