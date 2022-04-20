from web import db
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.ext.hybrid import hybrid_property
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

class Device(Base):
    __tablename__ = 'devices'

    pihole_device_id: int
    name: str

    pihole_device_id = db.Column(db.Integer)
    name = db.Column(db.String)
    def __repr__(self):
        return '<Device %r>' % (self.id)          
                      
@dataclass
class Traffic(db.Model):
    __tablename__ = 'traffic'
    id: int
    src: str
    dst: str
    proto: str
    service: str
    size: int
    date_created: datetime

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(3),  default=db.func.current_timestamp())
    src = db.Column(db.String(128))
    dst = db.Column(db.String(128))
    _proto = db.Column('proto', db.Boolean)
    service = db.Column(db.String(16), nullable=True)
    size = db.Column(db.SmallInteger())

    @hybrid_property
    def proto(self):
        return 'tcp' if self._proto==0 else 'udp'

    @proto.setter
    def proto(self, value):
        self._proto = 0 if value == 'tcp' else 1


    def __repr__(self):
        return '<Traffic %r>' % (self.id)                        
