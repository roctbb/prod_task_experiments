from flask import Flask, jsonify
from config import *
from flask_migrate import Migrate
from models import db
from schemas import *
from flask_pydantic import validate


app = Flask(__name__)

db_string = "postgresql://{}:{}@{}:{}/{}".format(POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['FLASK_PYDANTIC_VALIDATION_ERROR_RAISE'] = True
# app.config['SQLALCHEMY_ECHO'] = APP_DEBUG

db.init_app(app)
migrate = Migrate(app, db)

