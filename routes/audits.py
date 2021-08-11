from flask.json import jsonify
from app.routes.acts import Act
from flask_restful import Resource, reqparse, request, inputs
from flask_login import login_user, login_required, current_user, logout_user
from flask_restful_swagger import swagger
from flask.views import MethodView
from app.models.audit import AuditModel, AuditModelRequest
from app.models.act import ActModel
from app.models.organization import OrganizationModel
from app.models.site import SiteModel
from app.models.question import QuestionModel
from app.models.answer import AnswerModel
from app.models.user import UserModel
from app.schemas.audit import audit_schema, audits_schema_minimal
from app.schemas.act import acts_schema_minimal
from datetime import datetime


_audit_parser = reqparse.RequestParser()
_audit_parser.add_argument(
    "name",
    type=str,
    required=False,
    help="This field cannot be blank"
)
_audit_parser.add_argument(
    "organization",
    type=int,
    required=True,
    help="This field cannot be blank"
)
_audit_parser.add_argument(
    "site",
    type=int,
    required=True,
    help="This field cannot be blank"
)
_audit_parser.add_argument(
    "assigned",
    required=False,
    help="This field may be blank"
)
_audit_parser.add_argument(
    "taken",
    required=False,
    help="This field may be blank"
)
_audit_parser.add_argument(
    "finalized",
    type=int,
    required=True,
    help="This field cannot be blank"
)
_audit_parser.add_argument(
    "active",
    type=bool,
    required=False,
    help="This field cannot be blank"
)
_audit_parser.add_argument(
    "act_id",
    type=int,
    required=True,
    help="This field cannot be blank"
)
_audit_parser.add_argument(
    "site_id",
    type=int,
    required=False,
    help="This field cannot be blank"
)

def addPageMetaData(audit):
        audit.users = UserModel.find_all()

class ListAudits(MethodView):
    
    @swagger.operation(
        notes='Get All Acts & Audits',
        responseClass=AuditModel.__name__,
        responseMessages=[
            {
              "code": 200,
              "message": "Return a list of all acts & audits"
            }
        ]
    )

    
    def get(self):
        audits = AuditModel.find_all()
        acts = ActModel.find_all()

        return jsonify({ "acts" : acts_schema_minimal.dump(acts),
                         "audits": audits_schema_minimal.dump(audits)}
        )


    @swagger.operation(
        notes='Create New Audit',
        responseClass=AuditModel.__name__,
        parameters=[
            {
              "name": "audit",
              "description": "Audit creation",
              "required": True,
              "dataType": AuditModelRequest.__name__,
              "paramType": "body",
            }
        ],
    )
    def post(self):
        
        data = _audit_parser.parse_args()

        #check if act exists in the database
        act = ActModel.find_by_id(data['act_id'])
        if act is None:
            return {'message': 'Act id not found'}, 404

        #check if organization exists in the database
        organization = OrganizationModel.find_by_id(data['organization'])
        if organization is None:
            return {'message': 'Organization id not found'}, 404


        #check if act exists in the database
        act = ActModel.find_by_id(data['act_id'])
        if act is None:
             return {'message': 'Act id not found'}, 404

        #check if organization exists in the database
        organization = OrganizationModel.find_by_id(data['organization'])
        if organization is None:
            return {'message': 'Organization id not found'}, 404

        #check if site exists in the database
        site = SiteModel.find_by_id(data['site'])
        if site is None:
            return {'message': 'Site id not found'}, 404

        now = datetime.now()

        audit = AuditModel(data)
        audit.name = act.name + now.strftime(" (%Y)")
        audit.assigned = datetime.utcnow()
        audit.act = act
        audit.organization = organization
        audit.site = site
        audit.assigned = datetime.utcnow()


        questions = QuestionModel.find_questions_by_act_id(act.id)
        for question in questions:
            answer = AnswerModel({})
            answer.question = question
            answer.position = question.position
            audit.answers.append(answer)

        audit.save_to_db()

        return  audit_schema.dump(audit), 200



class ListAuditById(MethodView):

    @swagger.operation(
        notes='Get Audits By Id',
        responseClass=AuditModel.__name__
    )

    def get(self, _id):
        audit = AuditModel.find_by_id(_id)
        if audit:
            addPageMetaData(audit)
            return audit_schema.dump(audit), 200
        return {'message': 'Audit not found'}, 404


    @swagger.operation(notes="update audit by ID",
    parameters=[
            {
                "name": "audit",
                "description": "The Id of the audit",
                "required": True,
                "allowMultiple": False,
                "dataType": AuditModelRequest.__name__,
                "paramType": "body",
            }
        ])
    # @login_required
    def put(self, _id):
        data = _audit_parser.parse_args()

        #check if organization exists in the database
        organizationRecord = OrganizationModel.find_by_id(data['organization'])
        if organizationRecord is None:
            return {'message': 'Organization id not found'}, 404

        actRecord = ActModel.find_by_id(data['act_id'])
        if actRecord is None:
             return {'message': 'Act id not found'}, 404

        
        audit = AuditModel.find_by_id(_id)
        if audit:
            audit.update_details(name = data['name'],
                               organization = organizationRecord,
                               finalized = data['finalized'],
                               site = data['site'],
                               act = actRecord)

            return audit_schema.dump(audit), 200
        return {'message': 'Audit not found'}, 404


    @swagger.operation(notes="delete audit by ID",
    parameters=[
            {
                "name": "_id",
                "description": "The Id of the act",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path",
            }
        ])
    # @login_required
    def delete(self, _id):
        audit = AuditModel.find_by_id(_id)
        if not audit:
                return {
                "message": "Audit not found"
            }, 404

        audit.remove_from_db()

        return {
            "message": "Audit id {} deleted!".format(_id)
        }, 200


class FinalizeAuditById(MethodView):

    @swagger.operation(notes="Finalize audit by ID",
                       parameters=[
                       ])
    @login_required
    def post(self, _id):

        audit = AuditModel.find_by_id(_id)
        if audit:
            audit.update_details(finalized=True,
                                 taken=datetime.utcnow())

            return audit_schema.dump(audit), 200
        return {'message': 'Audit not found'}, 404
