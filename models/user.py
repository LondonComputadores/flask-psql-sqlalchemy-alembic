from app.database.db import db
from flask_restful_swagger import swagger
from flask_restful import fields
from flask_bcrypt import Bcrypt
import sqlalchemy
from sqlalchemy import func
from flask_login import UserMixin
from app.models.country import CountryModel
from app.models.state import StateModel
from datetime import datetime
from app.models.base_model import BaseModel


@swagger.model
class UserModel(db.Model, UserMixin, BaseModel):

    '''
    description: User description
    '''

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    city = db.Column(db.String(80))
    zip = db.Column(db.String(10))
    country_id = db.Column(
        db.Integer, db.ForeignKey('country_codes.id'), nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state_codes.id'), nullable=True)
    active = db.Column(db.Boolean, unique=False, nullable=False, default=True, server_default = 'true')
    created_at = db.Column(db.DateTime, default= datetime.utcnow, server_default = 'NOW()')
    updated_at = db.Column(db.DateTime(), default= datetime.utcnow)


    country = db.relationship(
        'CountryModel', lazy=True, foreign_keys=country_id)

    state = db.relationship(
        'StateModel', lazy=True, foreign_keys=state_id)

    resource_fields = {
        'id': fields.Integer,
        'email': fields.String,
        'password': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'phone': fields.String,
        'mobile': fields.String,
        'city': fields.String,
        'zip': fields.String,
    }

    required = ["email", "password", "first_name" ,"last_name"]

    def __init__(self, data):
        self.email = data.get('email', None)
        self.first_name = data.get('first_name', None)
        self.last_name = data.get('last_name', None)
        if 'password' in data and data['password']:
            bcrypt = Bcrypt()
            self.password = bcrypt.generate_password_hash(data['password'])
            self.password = self.password.decode('utf8')

        self.phone = data.get('phone', None)
        self.mobile = data.get('mobile', None)
        self.city = data.get('city', None)
        self.zip = data.get('zip', None)


    # Class method which finds user from DB by email
    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter(func.lower(UserModel.email)==func.lower(email)).first()


    # Class method which return all users
    @classmethod
    def find_all(cls):
        return cls.query.filter_by().all()

    def update_password(self, password):
        bcrypt = Bcrypt()
        self.password = bcrypt.generate_password_hash(password)
        self.password = self.password.decode('utf8')
        db.session.commit()

    @classmethod
    def count_users(cls):
        return cls.query.count()

sqlalchemy.orm.configure_mappers()



@swagger.model
class UserLoginRequest(UserMixin):
    __abstract__ = True
    '''
    description: User login request model
    '''

    resource_fields = {
        'email': fields.String,
        'password': fields.String,
    }

    required = ["email", "password"]

@swagger.model
class UserRegisterRequest(UserMixin):
    __abstract__ = True
    '''
    description: User register request model
    '''

    resource_fields = {
        'email': fields.String,
        'password': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'phone': fields.String,
        'mobile': fields.String,
        'city': fields.String,
        'zip': fields.String,
        'country': fields.Integer,
        'state': fields.Integer
    }

    required = ["email", "password", "first_name" ,"last_name"]
