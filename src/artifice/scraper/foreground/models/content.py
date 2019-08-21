from .base import BaseModel, db

class Content(BaseModel):
    __tablename__ = 'content'
    origin =        db.Column(db.String(500), unique=True, nullable=False)
    title =         db.Column(db.String(500))
    text =          db.Column(db.Text())
    captions =      db.Column(db.Text())
