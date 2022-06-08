from web import db
from dataclasses import dataclass
from datetime import datetime

from resolver.helpers import get_dhcp_leases

@dataclass
class PiHoleDevice(db.Model):
    __tablename__ = 'network'
    __bind_key__ = 'pihole'
    id: int
    hwaddr: str
    interface: str
    firstSeen: int
    lastQuery: int
    numQueries: int
    macVendor: str
    addresses: list
    name: str
    ip: str

    id = db.Column(db.Integer, primary_key=True)
    hwaddr = db.Column(db.String)
    interface = db.Column(db.String)
    firstSeen = db.Column(db.Integer)
    lastQuery = db.Column(db.Integer)
    numQueries = db.Column(db.Integer)
    macVendor = db.Column(db.String)
    addresses = db.relationship("NetworkAddress", primaryjoin='NetworkAddress.network_id == PiHoleDevice.id',
                                foreign_keys='NetworkAddress.network_id', order_by="desc(NetworkAddress.lastSeen)")

    @property
    def name(self):
        name = None
        for address in self.addresses:
            if(address.name is not None):
                name = address.name
                break
        return name
    @property
    def ip(self):
        addresses = []
        dhcp_leases = get_dhcp_leases()
        if(self.hwaddr) in dhcp_leases:
            return dhcp_leases[self.hwaddr]
        if len(self.addresses) > 0:
            return self.addresses[0].ip
    def __repr__(self):
        return '<PiHoleDevice %r>' % (self.id)

    def get_query():
        return PiHoleDevice.query.filter_by(interface='eth1')

    def get_all():
        return PiHoleDevice.query().all()

    def get_from_hwaddr(hwaddr):
        return PiHoleDevice.query().filter_by(hwaddr=hwaddr).all()


@dataclass
class NetworkAddress(db.Model):
    __tablename__ = 'network_addresses'
    __bind_key__ = 'pihole'
    network_id: int
    ip: str
    name: str
    lastSeen: int

    network_id = db.Column(db.Integer)
    ip = db.Column(db.String, primary_key=True)
    name = db.Column(db.Integer)
    lastSeen = db.Column(db.Integer)

    def __repr__(self):
        return '<Address %r>' % (self.id)
