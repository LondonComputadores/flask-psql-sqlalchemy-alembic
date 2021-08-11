from app.database.db import db

from flask_restful_swagger import swagger
from flask_restful import fields
import sqlalchemy
from datetime import datetime
from flask_login import UserMixin
from app.models.base_model import BaseModel

@swagger.model
class StateModel(db.Model, UserMixin, BaseModel):

    '''
    description: State Model description
    '''

    __tablename__ = "state_codes"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    position = db.Column(db.Integer, nullable=True, unique=False)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default= datetime.utcnow )

    resource_fields = {
        'id': fields.Integer,
        'code': fields.String,
        'name': fields.String,
        'active': fields.String,
        'position': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    required = ['name']

    def __init__(self, data):
        self.name = data['name']
        self.active = True


sqlalchemy.orm.configure_mappers()

# @event.listens_for(ActModel, 'before_update')
# def update_modified_on_update_listener(mapper, connection, target):
#     """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
#     target.updated_at = datetime.utcnow()