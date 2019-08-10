import os
import datetime

from . import db

class Queue(db.Model):
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
    modified_at = db.Column(db.DateTime(),nullable=True, onupdate=datetime.datetime.utcnow())
    url = db.Column(db.String(500), nullable=False, unique=True)
    tombstone = db.Column(db.Boolean(), nullable=True, default=False)
