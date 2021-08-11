from app.models.base_model import BaseModel
from app.database.db import db

from flask_restful_swagger import swagger
from flask_restful import fields
from flask_bcrypt import Bcrypt
import sqlalchemy
from datetime import datetime
from sqlalchemy import event
from flask_login import UserMixin

@swagger.model
class IncidentTypeModel(UserMixin, db.Model, BaseModel):

    '''
    description: Incident types model
    '''

    __tablename__ = "incident_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=False)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default= datetime.utcnow )
    position = db.Column(db.Integer)


    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'position': fields.Integer,
        'active': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    

    required = ['name']


    def __init__(self, data):
        self.name = data.get('name', None)
        self.position = data.get('position', None)
        BaseModel.__init__(self, data)


sqlalchemy.orm.configure_mappers()