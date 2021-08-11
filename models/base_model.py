from app.database.db import db
from flask_restful_swagger import swagger
from flask_restful import fields
from flask_bcrypt import Bcrypt
import sqlalchemy
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func, text, event
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):

    __abstract__ = True
    '''
    description: Base model
    '''


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
    def find_all(cls, order_by = 'id'):
        return cls.query.filter_by(active=True).order_by(order_by).all()

    
    # Method to update a record on DB
    def update_details(self,  **kwargs):
        updated_fields = 0
        for key, value in kwargs.items():
            setattr(self, key, value)
            updated_fields += 1
        if updated_fields > 0:
            db.session.commit()
            return True

        return False



sqlalchemy.orm.configure_mappers()