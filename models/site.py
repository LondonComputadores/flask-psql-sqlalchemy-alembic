from app.database.db import db

from flask_restful_swagger import swagger
from flask_restful import fields
from flask_bcrypt import Bcrypt
import sqlalchemy
from datetime import datetime
from sqlalchemy import event
from flask_login import UserMixin


@swagger.model
class SiteModel(db.Model, UserMixin):

    '''
    description: Site model
    '''

    __tablename__ = "sites"
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey(
        'organizations.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    address_1 = db.Column(db.String(255), nullable=True, unique=False)
    address_2 = db.Column(db.String(255), nullable=True, unique=False)
    city = db.Column(db.String(255), nullable=True, unique=False)
    state = db.Column(db.String(255), nullable=True, unique=False)
    country = db.Column(db.String(255), nullable=True, unique=False)
    zip = db.Column(db.String(5), nullable=True, unique=False)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default= datetime.utcnow )

    organization = db.relationship(
        'OrganizationModel', lazy=True, foreign_keys=org_id)


    resource_fields = {
        'id': fields.Integer,
        'organization': fields.Integer,
        'name': fields.String,
        'address_1': fields.String,
        'address_2': fields.String,
        'city': fields.String,
        'state': fields.String,
        'country': fields.String,
        'zip': fields.String,
        'active': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    required = ['organization', 'name']

    def __init__(self, data):
        self.name = data['name']
        self.address_1 = data['address_1']
        self.address_2 = data['address_2']
        self.city = data['city']
        self.state = data['state']
        self.country = data['country']
        self.zip = data['zip']
        self.active = True


    # Method to save act to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove act from DB
    def remove_from_db(self):
        self.active = False
        db.session.commit()


    # Class method which finds act from DB by id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).filter_by(active=True).first()


    # Class method which return all sites
    @classmethod
    def find_all(cls):
        return cls.query.filter_by(active=True).order_by(cls.id).all()



sqlalchemy.orm.configure_mappers()

@swagger.model
class SiteModelRequest():

    __abstract__ = True
    '''
    description: Site request for creating new record
    '''

    resource_fields = {
        'organization': fields.Integer,
        'name': fields.String,
        'address_1': fields.String,
        'address_2': fields.String,
        'city': fields.String,
        'state': fields.String,
        'country': fields.String,
        'zip': fields.String
    }

    required = ['organization', 'name']