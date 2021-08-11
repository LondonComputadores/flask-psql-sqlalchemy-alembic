from app.database.db import db

from flask_restful_swagger import swagger
from flask_restful import fields
from flask_bcrypt import Bcrypt
import sqlalchemy
from datetime import datetime
from sqlalchemy import event
from flask_login import UserMixin
from app.models.base_model import BaseModel
from app.models.incidents.incident_status import IncidentStatusModel
from app.models.incidents.incident_type import IncidentTypeModel

@swagger.model
class IncidentModel(db.Model, UserMixin, BaseModel):

    '''
    description: Incident model
    '''

    __tablename__ = "incidents"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=False)
    org_id = db.Column(db.Integer, db.ForeignKey(
        'organizations.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey(
        'sites.id'), nullable=False)
    description = db.Column(db.String(), nullable=True, unique=False)
    reported_at = db.Column(db.DateTime(), nullable=True, unique=False)
    discovered_at = db.Column(db.DateTime(), nullable=True, unique=False)
    resolved_at = db.Column(db.DateTime(), nullable=True, unique=False)
    occured_at = db.Column(db.DateTime(), nullable=True, unique=False)
    affected = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    reported_by_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=True)
    incident_type_id = db.Column(db.Integer, db.ForeignKey(
        'incident_types.id'), nullable=True)
    incident_status_id = db.Column(db.Integer, db.ForeignKey(
        'incident_status.id'), nullable=True)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default= datetime.utcnow )

    organization = db.relationship(
        'OrganizationModel', lazy=True, foreign_keys=org_id)

    site = db.relationship(
        'SiteModel', lazy=True, foreign_keys=site_id)

    reported_by = db.relationship(
        'UserModel', lazy=True, foreign_keys=reported_by_id)

    incident_type = db.relationship(
        'IncidentTypeModel', lazy=True, foreign_keys=incident_type_id)

    incident_status = db.relationship(
        'IncidentStatusModel', lazy=True, foreign_keys=incident_status_id)

    
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'organization': fields.Integer,
        'site': fields.Integer,
        'description': fields.String,
        'reported_at': fields.DateTime,
        'discovered_at': fields.DateTime,
        'resolved_at': fields.DateTime,
        'occured_at': fields.DateTime,
        'affected': fields.Boolean,
        'reported_by' : fields.Integer,
        'incident_type': fields.Integer,
        'incident_status': fields.Integer,
        'active': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    

    required = ['organization', 'site' 'name', 'incident_type', 'incident_status']



    def __init__(self, data):
        self.name = data.get('name', None)
        self.description = data.get('description', None)
        self.reported_at = data.get('reported_at', None)
        self.discovered_at = data.get('discovered_at', None)
        self.incident_type = data.get('incident_type', None)
        self.resolved_at = data.get('resolved_at', None)
        self.occured_at = data.get('occured_at', None)
        self.affected = data.get('affected', None)
        self.incident_status = data.get('incident_status', None)
        self.active = True


    @classmethod
    def count_incidents(cls):
        return cls.query.count()


sqlalchemy.orm.configure_mappers()

@swagger.model
class IncidentModelRequest():

    __abstract__ = True
    '''
    description: Site request for creating new record
    '''

    resource_fields = {
        'name': fields.String,
        'organization': fields.Integer,
        'site': fields.Integer,
        'description': fields.String,
        'reported_at': fields.DateTime,
        'discovered_at': fields.DateTime,
        'resolved_at': fields.DateTime,
        'occured_at': fields.DateTime,
        'affected': fields.Boolean,
        'reported_by' : fields.Integer,
        'incident_type': fields.Integer,
        'incident_status': fields.Integer
    }

    required = ['organization', 'site' 'name', 'incident_type', 'incident_status']