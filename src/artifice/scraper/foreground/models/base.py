import datetime

from .. import db

class BaseModel(db.Model):
    __abstract__ = True
    id =            db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    created_at =    db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
    modified_at =   db.Column(db.DateTime(),nullable=True, onupdate=datetime.datetime.utcnow())
