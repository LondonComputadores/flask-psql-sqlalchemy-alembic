from app.database.db import db

from flask_restful_swagger import swagger
from flask_restful import fields
from flask_bcrypt import Bcrypt
import sqlalchemy
from datetime import datetime
from sqlalchemy import func, text, event
from flask_login import UserMixin
from app.models.base_model import BaseModel
from app.models.question import QuestionModel
import enum

class Answer(enum.Enum):
    UNANSWERED = "UNANSWERED"
    YES = "YES"
    NO = "NO"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    ASSIGN = "ASSIGN"


@swagger.model
class AnswerModel(db.Model, UserMixin, BaseModel):

    '''
    description: Audit question answer
    '''

    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Enum(Answer), nullable=True, unique=False,  server_default=Answer.UNANSWERED.value)
    explanation = db.Column(db.String(1024), nullable=True, unique=False)
    notes = db.Column(db.String(1024), nullable=True, unique=False)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True)
    position = db.Column(db.Integer, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default= datetime.utcnow )
    audit_id = db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    assigned_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # audit = db.relationship('AuditModel', lazy=True, foreign_keys=audit_id)
    question = db.relationship('QuestionModel', lazy=True, foreign_keys=question_id)
    assigned = db.relationship('UserModel', lazy=True, foreign_keys=assigned_id)


    resource_fields = {
        'id': fields.Integer,
        'answer' : fields.String,
        'question': fields.String,
        'active': fields.Boolean,
        'position': fields.Boolean,
        'explanation': fields.String,
        'notes': fields.String,
        'assigned': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    required = ['question']

    def __init__(self, data):
        self.answer = Answer.UNANSWERED
        self.active = True



sqlalchemy.orm.configure_mappers()

@swagger.model
class AnswerModelRequest():

    __abstract__ = True
    '''
    description: Question request for creating new record
    answer should be one of the follwing: UNANSWERED, YES, NO, NOT_APPLICABLE, ASSIGN
    '''

    resource_fields = {
        'answer' : fields.String,
        'explanation': fields.String,
        'notes': fields.String,
        'assigned': fields.Integer
    }

    required = ['answer']

# @event.listens_for(ActModel, 'before_update')
# def update_modified_on_update_listener(mapper, connection, target):
#     """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
#     target.updated_at = datetime.utcnow()