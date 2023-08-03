from . import db
from flask_login import UserMixin
from sqlalchemy.schema import Column
from sqlalchemy.types import INTEGER, String



class User(db.Model, UserMixin):
    id = Column(INTEGER, primary_key=True)
    email = Column(String(150), unique=True)
    password = Column(String(150))
    name = Column(String(150))
    
