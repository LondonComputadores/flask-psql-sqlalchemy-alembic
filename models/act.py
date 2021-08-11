from app.database.db import db

from flask_restful_swagger import swagger
from flask_restful import fields
from flask_bcrypt import Bcrypt
import sqlalchemy
from datetime import datetime
from sqlalchemy import func, text, event
from flask_login import UserMixin
from app.models.base_model import BaseModel

@swagger.model
class ActModel(db.Model, UserMixin, BaseModel):

    '''
    description: Regulatory acts description
    '''

    __tablename__ = "acts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    org_wide = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default= datetime.utcnow )


    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'active': fields.Boolean,
        'org_wide': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    required = ['name', 'org_wide']

    def __init__(self, data):
        self.name = data['name']
        self.org_wide = data['org_wide']
        self.active = True



sqlalchemy.orm.configure_mappers()

@swagger.model
class ActModelRequest():

    __abstract__ = True
    '''
    description: Acts request for creating new record
    '''

    resource_fields = {
        'name': fields.String,
        'org_wide': fields.Boolean
    }

    required = ['name', 'org_wide']

# @event.listens_for(ActModel, 'before_update')
# def update_modified_on_update_listener(mapper, connection, target):
#     """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
#     target.updated_at = datetime.utcnow()