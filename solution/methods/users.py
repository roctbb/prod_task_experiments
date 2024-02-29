from models import User, db
from helpers import transaction
from exceptions import NotUnique


@transaction
def create_user(query):
    login_user = User.query.filter(
        (User.login == query.login) | (User.email == query.email)).first()
    phone_user = User.query.filter(User.phone == query.phone).first()

    if login_user or phone_user:
        raise NotUnique

    user = User(login=query.login, email=query.email, password=query.password, countryCode=query.countryCode,
                isPublic=query.isPublic, phone=query.phone, image=query.image)
    db.session.add(user)

    return user
