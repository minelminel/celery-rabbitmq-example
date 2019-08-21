from .base import BaseModel, db

class Queue(BaseModel):
    __tablename__ = 'queue'
    url =           db.Column(db.String(500), nullable=False, unique=True)
    status =        db.Column(db.String(10), nullable=False, default='READY')
