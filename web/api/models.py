from email.mime import base

from pyparsing import List
from web import db
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.ext.hybrid import hybrid_property
from web.pihole.models import PiHoleDevice
from pihole.helpers import get_dhcp_leases


class Base(db.Model):
    __abstract__ = True
    # Exported using dataclass
    id: int
    # table columns
    id = db.Column(db.Integer, primary_key=True)


class Timestamps(Base):
    __abstract__ = True
    date_created: datetime
    date_modified: datetime
    # table columns
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())


@dataclass
class Device(Timestamps):
    __tablename__ = 'devices'
    id: int
    pihole_device_id: int
    pihole_device: PiHoleDevice
    device_type_id: int
    device_type: object
    name: str
    hwaddr: str
    ip: str
    rules: list
    functionalities: List
    pihole_device_id = db.Column(db.Integer)
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_types.id'))
    name = db.Column(db.String)

    rules = db.relationship('Rule', back_populates="device")
    functionalities = db.relationship(
        'Functionality', secondary="device_functionalities")
    device_type = db.relationship('DeviceType', back_populates="devices")

    def __repr__(self):
        return '<Device %r>' % (self.id)

    @property
    def pihole_device(self):
        return PiHoleDevice.query.get(self.pihole_device_id)

    @property
    def hwaddr(self):
        return self.pihole_device.hwaddr

    @property
    def ip(self):
        addresses = []
        dhcp_leases = get_dhcp_leases()
        if(self.pihole_device.hwaddr) in dhcp_leases:
            return dhcp_leases[self.pihole_device.hwaddr]
        if len(self.pihole_device.addresses) > 0:
            return self.pihole_device.addresses[0].ip


@dataclass
class Rule(Timestamps):
    __tablename__ = 'rules'
    id: int
    device_id: int
    service: str

    device_id = db.Column(db.Integer,  db.ForeignKey('devices.id'))
    service = db.Column(db.String(128))

    device = db.relationship('Device', back_populates="rules")

    def __repr__(self):
        return '<Rule %r>' % (self.id)


@dataclass
class Traffic(Base):
    __tablename__ = 'traffic'
    id: int
    src: str
    dst: str
    proto: str
    service: str
    size: int
    date_created: datetime

    date_created = db.Column(db.DateTime(
        3),  default=db.func.current_timestamp())
    src = db.Column(db.String(128))
    dst = db.Column(db.String(128))
    _proto = db.Column('proto', db.Boolean)
    service = db.Column(db.String(16), nullable=True)
    size = db.Column(db.SmallInteger())

    @hybrid_property
    def proto(self):
        return 'tcp' if self._proto == 0 else 'udp'

    @proto.setter
    def proto(self, value):
        self._proto = 0 if value == 'tcp' else 1

    def __repr__(self):
        return '<Traffic %r>' % (self.id)


@dataclass
class DeviceType(Base):
    __tablename__ = 'device_types'
    id: str
    name: str
    type: str
    logo: str
    name = db.Column(db.String())
    type = db.Column(db.String())
    logo = db.Column(db.String())

    devices = db.relationship('Device', back_populates="device_type")
    functionalities = db.relationship('Functionality')

    def __repr__(self):
        return '<DeviceType %r>' % (self.id)


@dataclass
class Functionality(Base):
    __tablename__ = 'functionalities'
    id: int
    device_type_id: int
    name: str
    services: list
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_types.id'))
    name = db.Column(db.String())

    deviceType = db.relationship(
        'DeviceType', back_populates="functionalities")

    services = db.relationship('Service', secondary="functionality_services")

    def __repr__(self):
        return '<Functionality %r>' % (self.id)


@dataclass
class DeviceFunctionality(Base):
    __tablename__ = 'device_functionalities'
    id: int
    device_id: int
    functionality_id: int
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    functionality_id = db.Column(
        db.Integer, db.ForeignKey('functionalities.id'))

    def __repr__(self):
        return '<DeviceFunctionality %r>' % (self.id)


@dataclass
class ServerGroup(Base):
    __tablename__ = 'server_groups'
    id: int
    name: str
    name = db.Column(db.String)
    locations: list
    companies: list

    locations = db.relationship('Location', secondary="servers")
    companies = db.relationship(
        'Company', secondary="servers", overlaps="locations")

    def __repr__(self):
        return '<ServerGroup %r>' % (self.id)


@dataclass
class Service(Base):
    __tablename__ = 'services'
    id: int
    device_type_id: int
    server_group_id: int
    cloud: bool
    device_type: DeviceType
    server_group: ServerGroup
    service_data: dict
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_types.id'))
    server_group_id = db.Column(db.Integer, db.ForeignKey('server_groups.id'))
    cloud = db.Column(db.Boolean)

    device_type = db.relationship('DeviceType')
    server_group = db.relationship('ServerGroup')
    service_data = db.relationship('ServiceData', back_populates="service")

    def __repr__(self):
        return '<Service %r>' % (self.id)


@dataclass
class FunctionalityService(Base):
    __tablename__ = 'functionality_services'
    id: int
    functionality_id: int
    service_id: int
    functionality_id = db.Column(
        db.Integer, db.ForeignKey('functionalities.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    # functionality = db.relationship('Functionality', overlaps="services")
    # service = db.relationship('Service', overlaps="services")

    def __repr__(self):
        return '<Service %r>' % (self.id)


@dataclass
class DataType(Base):
    __tablename__ = 'data_types'
    id: int
    name: str
    icon: str
    name = db.Column(db.String)
    icon = db.Column(db.String)

    def __repr__(self):
        return '<DataType %r>' % (self.id)


@dataclass
class ServiceData(Base):
    __tablename__ = 'service_data'
    id: int
    service_id: int
    data_type_id: int
    data_type: DataType
    storage: str
    trigger: str
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    data_type_id = db.Column(db.Integer, db.ForeignKey('data_types.id'))
    storage = db.Column(db.String)
    trigger = db.Column(db.String)

    service = db.relationship('Service')
    data_type = db.relationship('DataType')

    def __repr__(self):
        return '<ServiceData %r>' % (self.id)


@dataclass
class ServerQuery(Base):
    __tablename__ = 'server_queries'
    id: int
    server_group_id: int
    ip: str
    domain: str
    server_group_id = db.Column(db.Integer, db.ForeignKey('server_groups.id'))
    ip = db.Column(db.String)
    domain = db.Column(db.String)

    server_group = db.relationship('ServerGroup')

    def __repr__(self):
        return '<ServerQuery %r>' % (self.id)

    @staticmethod
    def find_server_group_id(domain, ip):
        server_query = ServerQuery.query
        if ip != None:
            server_query = server_query.filter(db.or_(
                ServerQuery.ip == None, db.bindparam('ip_query', ip).contains(ServerQuery.ip)))
        if domain != None:
            server_query = server_query.filter(db.or_(ServerQuery.domain == None, db.bindparam(
                'domain_query', domain).contains(ServerQuery.domain)))
        result = server_query.first()
        if not result:
            return None
        return result.server_group_id


@dataclass
class Company(Base):
    __tablename__ = 'companies'
    id: int
    name: str
    name = db.Column(db.String)

    servers = db.relationship(
        'Server',  back_populates="company", overlaps="companies")

    def __repr__(self):
        return '<Company %r>' % (self.id)


@dataclass
class Location(Base):
    __tablename__ = 'locations'
    id: int
    city: str = db.Column(db.String)
    region: str = db.Column(db.String)
    country: str = db.Column(db.String)
    continent: str = db.Column(db.String)
    lat: float = db.Column(db.String)
    lon: float = db.Column(db.String)

    def __repr__(self):
        return '<Location %r>' % (self.id)


@dataclass
class Server(Base):
    __tablename__ = 'servers'
    id: int
    server_group_id: int
    company_id: int
    location_id: int
    ip: str
    server_group: ServerGroup
    company: Company
    location: Location

    server_group_id = db.Column(db.Integer, db.ForeignKey('server_groups.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    ip = db.Column(db.String)

    server_group = db.relationship(
        'ServerGroup', overlaps="companies,locations")
    company = db.relationship(
        'Company',  back_populates="servers", overlaps="companies")
    location = db.relationship('Location', overlaps="locations")

    def __repr__(self):
        return '<Server %r>' % (self.id)


@dataclass
class Domain(Base):
    __tablename__ = 'domains'
    id: int
    server_id: int
    name: str

    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'))
    name = db.Column(db.String)

    server = db.relationship('Server')

    def __repr__(self):
        return '<ServerQuery %r>' % (self.id)
