from flask_restful import Resource, reqparse, request, inputs
from flask_login import login_user, login_required, current_user, logout_user
from flask_restful_swagger import swagger
from flask.views import MethodView
from app.database.db import db
from datetime import datetime
from app.models.audit import AuditModel, AuditModelRequest
from app.models.act import ActModel
from app.models.organization import OrganizationModel
from app.models.answer import AnswerModel, AnswerModelRequest, Answer
from app.models.user import UserModel
from app.schemas.answer import answer_schema
from app.schemas.organization import organization_schema, organizations_schema


_answer_parser = reqparse.RequestParser()
_answer_parser.add_argument(
    "answer",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_answer_parser.add_argument(
    "notes",
    type=str,
    required=False,
    help="This field cannot be blank"
)
_answer_parser.add_argument(
    "explanation",
    type=str,
    required=False,
    help="This field cannot be blank"
)
_answer_parser.add_argument(
    "assigned",
    type=int,
    required=False
)


class ListAnswersById(MethodView):

    @swagger.operation(
        notes='Get Answer By Id',
        responseClass=AnswerModel.__name__
    )

    def get(self, _id):
        audit = AnswerModel.find_by_id(_id)
        if audit:
            return answer_schema.dump(audit), 200
        return {'message': 'Answer not found'}, 404


    @swagger.operation(notes="Update answer by id",
    parameters=[
            {
                "name": "answer",
                "description": "Answer should be one of the follwing: UNANSWERED, YES, NO, NOT_APPLICABLE, ASSIGN",
                "required": True,
                "allowMultiple": False,
                "dataType": AnswerModelRequest.__name__,
                "paramType": "body",
            }
        ])
    # @login_required
    def put(self, _id):
        data = _answer_parser.parse_args()

        assignedRecord = None
        if (data['assigned']):
            assignedRecord = UserModel.find_by_id(data['assigned'])

    
        answer = AnswerModel.find_by_id(_id)
        if answer:
            answer.update_details(answer = Answer(data['answer']),
                               notes = data['notes'],
                               explanation = data['explanation'],
                               assigned = assignedRecord)

            return answer_schema.dump(answer), 200
        return {'message': 'Audit not found'}, 404