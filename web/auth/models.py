from web import db
from datetime import datetime
from dataclasses import dataclass
@dataclass
class Base(db.Model):
    __abstract__  = True
    # Exported using dataclass
    id: int
    date_created: datetime
    date_modified: datetime
    # table columns
    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
class User(Base):

    __tablename__ = 'users'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)

    def __repr__(self):
        return '<User %r>' % (self.name)                            