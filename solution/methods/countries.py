from models import Country


def find_country(alpha2):
    return Country.query.filter_by(alpha2=alpha2).first_or_404()


def fetch_countries(regions=[]):
    if not regions:
        return Country.query.order_by(Country.alpha2).all()
    else:
        return Country.query.filter(Country.region.in_(regions)).order_by(Country.alpha2).all()
