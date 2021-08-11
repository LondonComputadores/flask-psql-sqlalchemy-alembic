from flask_restful import reqparse
from flask_login import login_user, login_required, current_user, logout_user
from flask_restful_swagger import swagger
from flask.views import MethodView
from app.database.db import db
from app.models.organization import OrganizationModel, OrganizationModelRequest
from app.schemas.organization import organization_schema, organizations_schema


_organization_parser = reqparse.RequestParser()
_organization_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_organization_parser.add_argument(
    "address_1",
    type=str,
    required=True,
    help="This field may be blank"
)
_organization_parser.add_argument(
    "address_2",
    type=str,
    required=True,
    help="This field may be blank"
)
_organization_parser.add_argument(
    "zip",
    type=str,
    required=True,
    help="This field may be blank"
)


class ListOrganizations(MethodView):

    @swagger.operation(
        notes='Get All Organizations',
        responseClass=OrganizationModel.__name__,
        responseMessages=[
            {
              "code": 200,
              "message": "Return a list of all acts"
            }
        ]
    )
    def get(self):
        organizations = OrganizationModel.find_all()
        return organizations_schema.dump(organizations), 200

    @swagger.operation(
        notes='Create Organization',
        responseClass=OrganizationModel.__name__,
        parameters=[
            {
              "name": "organization",
              "description": "Organization name",
              "required": True,
              "dataType": OrganizationModelRequest.__name__,
              "paramType": "body",
            }
        ],
    )
    def post(self):

        data = _organization_parser.parse_args()

        organization = OrganizationModel(data)
        organization.save_to_db()

        return organization_schema.dump(organization), 200


class ListOrganizationById(MethodView):

    @swagger.operation(notes="Gets organization by id",
                       parameters=[
                           {
                               "name": "_id",
                               "description": "The Id of the organization",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": "string",
                               "paramType": "path",
                           }
                       ],
                       responseMessages=[
                           {
                               "code": 200,
                               "message": "Organization object"
                           },
                           {
                               "code": 404,
                               "message": "Organization not found"
                           }
                       ])
    # @login_required
    def get(self, _id):
        organization = OrganizationModel.find_by_id(_id)

        if (organization is None):
            return {
                "message": "Organization id {} not found!".format(_id)
            }, 404

        return organization_schema.dump(organization), 200

    @swagger.operation(notes="delete organization by ID",
                       parameters=[
                           {
                               "name": "_id",
                               "description": "The Id of the organization",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": "string",
                               "paramType": "path",
                           }
                       ],
                       responseMessages=[
                           {
                               "code": 200,
                               "message": "Organization deleted!"
                           },
                           {
                               "code": 404,
                               "message": "Organization not found"
                           }
                       ])
    # @login_required
    def delete(self, _id):
        organization = OrganizationModel.find_by_id(_id)

        if not organization:
            return {
                "message": "Organization not found"
            }, 404

        organization.remove_from_db()

        return {
            "message": "Organization id {} deleted!".format(_id)
        }, 200
