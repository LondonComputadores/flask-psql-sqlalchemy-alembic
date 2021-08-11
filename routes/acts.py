from flask_restful import reqparse
from flask_login import login_user, login_required, current_user, logout_user
from flask_restful_swagger import swagger
from flask.views import MethodView
from app.models.act import ActModel, ActModelRequest
from app.schemas.act import act_schema, acts_schema


_acts_parser = reqparse.RequestParser()
_acts_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_acts_parser.add_argument(
    "org_wide",
    type=bool,
    required=True,
    help="This field cannot be blank"
)


class ListActs(MethodView):

    @swagger.operation(
        notes='Get All Regulatory Act',
        responseClass=ActModel.__name__,
        responseMessages=[
            {
              "code": 200,
              "message": "Return a list of all acts"
            }
        ]
    )
    def get(self):
        acts = ActModel.find_all()
        return acts_schema.dump(acts), 200

    @swagger.operation(
        notes='Create Regulatory Act',
        responseClass=ActModel.__name__,
        parameters=[
            {
              "name": "act",
              "description": "Act name and org wide",
              "required": True,
              "dataType": ActModelRequest.__name__,
              "paramType": "body",
            }
        ],
    )
    def post(self):

        data = _acts_parser.parse_args()

        act = ActModel(data)
        act.save_to_db()

        return act_schema.dump(act), 200


class Act(MethodView):

    @swagger.operation(notes="Gets act by id",
                       parameters=[
                           {
                               "name": "_id",
                               "description": "The Id of the act",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": "string",
                               "paramType": "path",
                           }
                       ],
                       responseMessages=[
                           {
                               "code": 200,
                               "message": "Act object"
                           },
                           {
                               "code": 404,
                               "message": "Act not found"
                           }
                       ])
    # @login_required
    def get(self, _id):
        act = ActModel.find_by_id(_id)

        if (act is None):
            return {
                "message": "Act id {} not found!".format(_id)
            }, 404

        return act_schema.dump(act), 200

    @swagger.operation(notes="delete regulatory act by ID",
                       parameters=[
                           {
                               "name": "act_id",
                               "description": "The Id of the act",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": "string",
                               "paramType": "path",
                           }
                       ],
                       responseMessages=[
                           {
                               "code": 200,
                               "message": "Act deleted!"
                           },
                           {
                               "code": 404,
                               "message": "Act not found"
                           }
                       ])
    # @login_required
    def delete(self, _id):
        act = ActModel.find_by_id(_id)

        if not act:
            return {
                "message": "Act not found"
            }, 404

        act.remove_from_db()

        return {
            "message": "Act id {} deleted!".format(_id)
        }, 200
