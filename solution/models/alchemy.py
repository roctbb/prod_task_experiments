from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime, timedelta
from sqlalchemy import desc

db = SQLAlchemy()