from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# pylint: disable-next=too-few-public-methods
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
