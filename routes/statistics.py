from flask.json import jsonify
from flask_restful import Resource, reqparse, request, inputs
from flask_login import login_user, login_required, current_user, logout_user
from flask_restful_swagger import swagger
from flask.views import MethodView
from app.database.db import db
from app.models.audit import AuditModel
from app.models.incidents.incident import IncidentModel
from app.models.user import UserModel
from app.schemas.statistics import AuditCounter, stat_counter, stats_counter
from app.schemas.statistics import IncidentCounter, stat_counter, stats_counter
from sqlalchemy import func
from app.schemas.audit import audit_schema, audits_schema_minimal


class Stats(MethodView):

    @swagger.operation(
        notes='Get All Statistics',
        responseClass=AuditModel.__name__,
        responseMessages=[
            {
              "code": 200,
              "message": "Return a list of all audits statistics"
            }
        ]
    )    
    def get(self):
        audits = AuditModel.count_audits()
        incidents = IncidentModel.count_incidents()
        # audits = AuditModel.count_audits()
        # audits = IncidentModel.count_audits()
        # audits = IncidentModel.count_audits()
        # audits = UserModel.count_audits()
        return jsonify(
            # {"Attestations": {
            #         "total" : AttestationsModel.count_audits(),
            #         "complete": 0
            #         }},
            {"Audits": {
                    "total" : AuditModel.count_audits(),
                    "complete": 0
                    }},
            {"Incidents": {
                    "total" : IncidentModel.count_incidents(),
                    "complete": 0
                    }},
            # {"Remediation": {
            #         "total" : RemediationModel.count_audits(),
            #         "complete": 0
            #         }},
            # {"Tasks": {
            #         "total" : TasksModel.count_audits(),
            #         "complete": 0
            #         }},
            {"Users": {
                    "users" : UserModel.count_users(),
                    "sites": 0
                    }},
            
            )

    