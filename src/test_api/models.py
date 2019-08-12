import os
import datetime

from . import db

class Queue(db.Model):
    __tablename__ = 'queue'

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    created_at =    db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
    modified_at =   db.Column(db.DateTime(),nullable=True, onupdate=datetime.datetime.utcnow())
    url =           db.Column(db.String(500), nullable=False, unique=True)
    tombstone =     db.Column(db.Boolean(), nullable=True, default=False)


class Content(db.Model):
    __tablename__ = 'content'

    id =            db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    created_at =    db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
    modified_at =   db.Column(db.DateTime(), nullable=True, onupdate=datetime.datetime.utcnow())
    origin =        db.Column(db.String(500), unique=True, nullable=False)
    title =         db.Column(db.String(500))
    text =          db.Column(db.Text())
    captions =      db.Column(db.Text())
