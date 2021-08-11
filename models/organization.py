from app.database.db import db

from flask_restful_swagger import swagger
from flask_restful import fields
from flask_bcrypt import Bcrypt
import sqlalchemy
from datetime import datetime
from sqlalchemy import event
from flask_login import UserMixin


@swagger.model
class OrganizationModel(db.Model, UserMixin):

    '''
    description: Organization model
    '''

    __tablename__ = "organizations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    address_1 = db.Column(db.String(255), nullable=True, unique=False)
    address_2 = db.Column(db.String(255), nullable=True, unique=False)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    zip = db.Column(db.String(5), nullable=True, unique=False)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default= datetime.utcnow )


    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'address_1': fields.String,
        'address_2': fields.String,
        'active': fields.Boolean,
        'zip': fields.String,
    }

    required = ['name', 'address_1', 'zip']

    def __init__(self, data):
        self.name = data['name']
        self.address_1 = data['address_1']
        self.address_2 = data['address_2']
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


    # Class method which return all acts
    @classmethod
    def find_all(cls):
        return cls.query.filter_by(active=True).order_by(cls.id).all()



sqlalchemy.orm.configure_mappers()

@swagger.model
class OrganizationModelRequest():

    __abstract__ = True
    '''
    description: Audits request for creating new record
    '''

    resource_fields = {
        'name': fields.String,
        'address_1': fields.String,
        'address_2': fields.String,
        'active': fields.Boolean,
        'zip': fields.String,
    }

    required = ['name', 'address_1', 'address_2', 'zip']

# @event.listens_for(ActModel, 'before_update')
# def update_modified_on_update_listener(mapper, connection, target):
#     """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
#     target.updated_at = datetime.utcnow()