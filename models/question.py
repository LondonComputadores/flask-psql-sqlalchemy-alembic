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
class QuestionModel(db.Model, UserMixin, BaseModel):

    '''
    description: Audit Question description
    '''

    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1024), nullable=False, unique=True)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    position = db.Column(db.Integer, nullable=True, unique=False)
    domain = db.Column(db.String(255), nullable=True, unique=False)
    cmmc_ref = db.Column(db.String(128), nullable=True, unique=False)
    nist_ref = db.Column(db.String(128), nullable=True, unique=False)
    nist_score = db.Column(db.Integer, nullable=True, unique=False)
    coaching = db.Column(db.String(4096), nullable=True, unique=False)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default= datetime.utcnow )
    act_id = db.Column(db.Integer, db.ForeignKey('acts.id'), nullable=False)

    act = db.relationship('ActModel', lazy=True, foreign_keys=act_id)


    resource_fields = {
        'id': fields.Integer,
        'question': fields.String,
        'domain': fields.String,
        'cmmc_ref': fields.String,
        'nist_ref': fields.String,
        'nist_score': fields.String,
        'coaching': fields.String,
        'active': fields.Boolean,
        'position': fields.Boolean,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    required = ['question']

    def __init__(self, data):
        self.question = data['question']
        self.active = True

    # Class method which return all questions for a regulatory act
    @classmethod
    def find_questions_by_act_id(cls, act_id):
        return cls.query.filter_by(active=True).filter_by(act_id=act_id).order_by(cls.position).all()



sqlalchemy.orm.configure_mappers()

@swagger.model
class QuestionRequest():

    __abstract__ = True
    '''
    description: Question request for creating new record
    '''

    resource_fields = {
        'question': fields.String,
    }

    required = ['question']

# @event.listens_for(ActModel, 'before_update')
# def update_modified_on_update_listener(mapper, connection, target):
#     """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
#     target.updated_at = datetime.utcnow()