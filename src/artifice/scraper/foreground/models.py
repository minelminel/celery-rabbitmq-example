import os
import datetime

from . import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    created_at =    db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
    modified_at =   db.Column(db.DateTime(),nullable=True, onupdate=datetime.datetime.utcnow())


class Queue(BaseModel):
    __tablename__ = 'queue'
    url =           db.Column(db.String(500), nullable=False, unique=True)
    status =     db.Column(db.String(10), nullable=False, default='READY')


class Content(BaseModel):
    __tablename__ = 'content'
    origin =        db.Column(db.String(500), unique=True, nullable=False)
    title =         db.Column(db.String(500))
    text =          db.Column(db.Text())
    captions =      db.Column(db.Text())
