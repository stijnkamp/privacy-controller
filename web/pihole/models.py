from web import db
from dataclasses import dataclass
from datetime import datetime
@dataclass
class Device(db.Model):
    __tablename__ = 'network'
    __bind_key__ = 'pihole'
    id: int
    hwaddr: str
    interface: str
    firstSeen: int
    lastQuery: int
    numQueries: int
    macVendor: str

    id = db.Column(db.Integer, primary_key=True)
    hwaddr = db.Column(db.String)
    interface = db.Column(db.String)
    firstSeen = db.Column(db.Integer)
    lastQuery = db.Column(db.Integer)
    numQueries = db.Column(db.Integer)
    macVendor = db.Column(db.String)
    def __repr__(self):
        return '<Device %r>' % (self.id)
    def get_query():
        return Device.query.filter_by(interface='eth1')
    def getAll():
        return Device.query().all()
    def getFromHwaddr(hwaddr):
        return Device.query().filter_by(hwaddr=hwaddr).all()