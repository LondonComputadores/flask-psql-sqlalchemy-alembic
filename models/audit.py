from app.database.db import db
from flask_restful_swagger import swagger
from flask_restful import fields
from flask_bcrypt import Bcrypt
import sqlalchemy
from sqlalchemy import func
from datetime import datetime
from flask_login import UserMixin
from app.models.answer import AnswerModel
from app.models.site import SiteModel
import logging
from app.models.base_model import BaseModel


@swagger.model
class AuditModel(db.Model, UserMixin, BaseModel):

    '''
    description: Audit description
    '''

    __tablename__ = "audits"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    org_id = db.Column(db.Integer, db.ForeignKey(
        'organizations.id'), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey(
        'sites.id'), nullable=True)
    assigned = db.Column(db.DateTime,  nullable=True)
    taken = db.Column(db.DateTime,  nullable=True)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    finalized = db.Column(db.Boolean, unique=False,
                          nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    act_id = db.Column(db.Integer, db.ForeignKey('acts.id'), nullable=False)

    act = db.relationship('ActModel', lazy=True, foreign_keys=act_id)
    organization = db.relationship(
        'OrganizationModel', lazy=True, foreign_keys=org_id)
    site = db.relationship(
        'SiteModel', lazy=True, foreign_keys=site_id)
    answers = db.relationship("AnswerModel", backref="audit",
    order_by="asc(AnswerModel.position)")

    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'organization': fields.Integer,
        'site': fields.Integer,
        'finalized': fields.Boolean,
        'active': fields.Boolean,
        'act_id': fields.Integer
    }

    required = ['name', 'act_id']

    def __init__(self, data):
        self.name = data['name']
        self.site = data['site']
        self.assigned = data['assigned']
        self.taken = data['taken']
        self.finalized = False
        self.active = True

    @classmethod
    def count_audits(cls):
        return cls.query.count()



sqlalchemy.orm.configure_mappers()


@swagger.model
class AuditModelRequest():

    __abstract__ = True
    '''
    description: Audits request for creating new record
    '''

    resource_fields = {
        'name': fields.String,
        'organization': fields.Integer,
        'site': fields.Integer,
        'finalized': fields.Boolean,
        'act_id': fields.Integer
    }

    required = ['name', 'organization']