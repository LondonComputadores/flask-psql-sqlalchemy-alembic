from app.database.ma import ma
from app.models.base_model import BaseModel
from app.models.audit import AuditModel
from app.models.incidents.incident import IncidentModel
from app.models.user import UserModel
from marshmallow import fields


# class AttestationsCounter(ma.SQLAlchemySchema):
#     class Meta:
#         model = AttestationsModel


class AuditCounter(ma.SQLAlchemySchema):
    class Meta:
        model = AuditModel


class IncidentCounter(ma.SQLAlchemySchema):
    class Meta:
        model = IncidentModel


class UserCounter(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel


# class RemediationCounter(ma.SQLAlchemySchema):
#     class Meta:
#         model = RemediationModel


# class TasksCounter(ma.SQLAlchemySchema):
#     class Meta:
#         model = TasksModel




# stat_counter = AttestationCounter()
# stats_counter = AttestationCounter(many=True)

stat_counter = AuditCounter()
stats_counter = AuditCounter(many=True)

stat_counter = IncidentCounter()
stats_counter = IncidentCounter(many=True)

# stat_counter = RemediationCounter()
# stats_counter = RemediationCounter(many=True)

# stat_counter = TasksCounter()
# stats_counter = TasksCounter(many=True)

stat_counter = UserCounter()
stats_counter = UserCounter(many=True)