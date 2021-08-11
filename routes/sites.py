from flask_restful import reqparse
from flask_login import login_user, login_required, current_user, logout_user
from flask_restful_swagger import swagger
from flask.views import MethodView
from app.models.organization import OrganizationModel
from app.models.site import SiteModel, SiteModelRequest
from app.schemas.site import site_schema, sites_schema


_sites_parser = reqparse.RequestParser()
_sites_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_sites_parser.add_argument(
    "organization",
    type=int,
    required=True,
    help="This field cannot be blank"
)
_sites_parser.add_argument(
    "address_1",
    type=str
)

_sites_parser.add_argument(
    "address_2",
    type=str
)

_sites_parser.add_argument(
    "city",
    type=str
)

_sites_parser.add_argument(
    "state",
    type=str
)

_sites_parser.add_argument(
    "country",
    type=str
)

_sites_parser.add_argument(
    "zip",
    type=str
)


class ListSites(MethodView):

    @swagger.operation(
        notes='Get All Sites',
        responseClass=SiteModel.__name__,
        responseMessages=[
            {
              "code": 200,
              "message": "Return a list of all sites"
            }
        ]
    )
    def get(self):
        sites = SiteModel.find_all()
        return sites_schema.dump(sites), 200

    @swagger.operation(
        notes='Create Site',
        responseClass=SiteModel.__name__,
        parameters=[
            {
              "name": "site",
              "description": "Org id and site name",
              "required": True,
              "dataType": SiteModelRequest.__name__,
              "paramType": "body",
            }
        ],
    )
    def post(self):

        data = _sites_parser.parse_args()

        #check if organization exists in the database
        organization = OrganizationModel.find_by_id(data['organization'])
        if organization is None:
            return {'message': 'Organization id not found'}, 404

        site = SiteModel(data)
        site.organization = organization
        site.save_to_db()

        return site_schema.dump(site), 200


class SiteById(MethodView):

    @swagger.operation(notes="Gets site by id",
                       parameters=[
                           {
                               "name": "_id",
                               "description": "The Id of the site",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": "string",
                               "paramType": "path",
                           }
                       ],
                       responseMessages=[
                           {
                               "code": 200,
                               "message": "Site object"
                           },
                           {
                               "code": 404,
                               "message": "Site not found"
                           }
                       ])
    # @login_required
    def get(self, _id):
        site = SiteModel.find_by_id(_id)

        if (site is None):
            return {
                "message": "Site id {} not found!".format(_id)
            }, 404

        return site_schema.dump(site), 200

    @swagger.operation(notes="delete site by ID",
                       parameters=[
                           {
                               "name": "_id",
                               "description": "The Id of the site",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": "string",
                               "paramType": "path",
                           }
                       ],
                       responseMessages=[
                           {
                               "code": 200,
                               "message": "Site deleted!"
                           },
                           {
                               "code": 404,
                               "message": "Act not found"
                           }
                       ])
    # @login_required
    def delete(self, _id):
        site = SiteModel.find_by_id(_id)

        if not site:
            return {
                "message": "Site not found"
            }, 404

        site.remove_from_db()

        return {
            "message": "Site id {} deleted!".format(_id)
        }, 200
