from flask.json import jsonify
from app.models.incidents.incident_status import IncidentStatusModel
from app.models.incidents.incident_type import IncidentTypeModel
from flask_restful import reqparse, inputs
from flask import jsonify
from flask_login import login_user, login_required, current_user, logout_user
from flask_restful_swagger import swagger
from flask.views import MethodView
from app.models.organization import OrganizationModel
from app.models.site import SiteModel
from app.models.user import UserModel
from app.models.incidents.incident import IncidentModel, IncidentModelRequest
from app.schemas.incidents.incident import incident_schema, incidents_schema
from datetime import datetime


_incident_parser = reqparse.RequestParser()
_incident_parser.add_argument(
    "name",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_incident_parser.add_argument(
    "organization",
    type=int,
    required=True,
    help="This field cannot be blank"
)

_incident_parser.add_argument(
    "site",
    type=int,
    required=True,
    help="This field cannot be blank"
)

_incident_parser.add_argument(
    "description",
    type=str
)

_incident_parser.add_argument(
    "reported_at",
    type=inputs.datetime_from_iso8601
)

_incident_parser.add_argument(
    "discovered_at",
    type=inputs.datetime_from_iso8601
)

_incident_parser.add_argument(
    "resolved_at",
    type=inputs.datetime_from_iso8601
)

_incident_parser.add_argument(
    "occured_at",
    type=inputs.datetime_from_iso8601
)

_incident_parser.add_argument(
    "affected",
    type=bool
)

_incident_parser.add_argument(
    "reported_by",
    type=int
)

_incident_parser.add_argument(
    "incident_type",
    type=int,
    required=True,
    help="This value is not valid"
)

_incident_parser.add_argument(
    "incident_status",
    type=int,
    required=True,
    help="This value is required"
)


_incident_update_parser = _incident_parser.copy()
_incident_update_parser.add_argument(
    "active",
    type=bool
)
_incident_update_parser.add_argument(
    "affected",
    type=bool,
    required=True,
    help="This value is not valid"
)

class ListIncidents(MethodView):

    @swagger.operation(
        notes='Get All Incidents',
        responseClass=IncidentModel.__name__,
        responseMessages=[
            {
              "code": 200,
              "message": "Return a list of all incidents"
            }
        ]
    )
    def get(self):
        incidents = IncidentModel.find_all()
        return jsonify({ "incidents": incidents_schema.dump(incidents)})

#This method contains all the data needed by the page for loading the dropdown choices
def addPageMetaData(incident):
        incident.incident_types = IncidentTypeModel.find_all()
        incident.incident_statuses = IncidentStatusModel.find_all()
        incident.users = UserModel.find_all()
        incident.sites = SiteModel.find_all()


class CreateIncident(MethodView):
    @swagger.operation(notes="Gets incident meta data only",
                       parameters=[
                       ],
                       responseMessages=[
                           {
                               "code": 200,
                               "message": "Incident object"
                           },
                       ])
    # @login_required
    def get(self):

        incident = IncidentModel({})
        addPageMetaData(incident)
        return incident_schema.dump(incident), 200

    @swagger.operation(
        notes='Create Incident',
        responseClass=IncidentModel.__name__,
        parameters=[
            {
              "name": "incident",
              "description": "Org id and site id and name of the incident",
              "required": True,
              "dataType": IncidentModelRequest.__name__,
              "paramType": "body",
            }
        ],
    )


    def post(self):

        data = _incident_parser.parse_args()

        #check if organization exists in the database
        organization = OrganizationModel.find_by_id(data['organization'])
        if organization is None:
            return {'message': 'Organization id not found'}, 404

        #check if site exists in the database
        site = SiteModel.find_by_id(data['site'])
        if site is None:
            return {'message': 'Site id not found'}, 404

        if (data['reported_by']):
            #check if user who reported the incident exists
            reported_by = UserModel.find_by_id(data['reported_by'])
            if reported_by is None:
                return {'message': 'User id not found'}, 404

        if (data['incident_type']):
             #check if incident type exists
            incident_type = IncidentTypeModel.find_by_id(data['incident_type'])
            if incident_type is None:
                return {'message': 'Incident type not found'}, 404

        if (data['incident_status']):
             #check if incident type exists
            incident_status = IncidentStatusModel.find_by_id(data['incident_status'])
            if incident_status is None:
                return {'message': 'Incident status not found'}, 404
        else:
            incident_status = IncidentStatusModel.find_default_value()
    
        incident = IncidentModel(data)
        incident.organization = organization
        incident.site = site
        incident.reported_by = reported_by
        incident.incident_type = incident_type
        incident.incident_status = incident_status
        incident.save_to_db()

        addPageMetaData(incident)
        return incident_schema.dump(incident), 200




class IncidentById(MethodView):

    @swagger.operation(notes="Gets incident by id",
                       parameters=[
                           {
                               "name": "_id",
                               "description": "The Id of the incident",
                               "required": False,
                               "allowMultiple": False,
                               "dataType": "string",
                               "paramType": "path",
                           }
                       ],
                       responseMessages=[
                           {
                               "code": 200,
                               "message": "Incident object"
                           },
                           {
                               "code": 404,
                               "message": "Incident not found"
                           }
                       ])
    # @login_required
    def get(self, _id):

        incident = IncidentModel.find_by_id(_id)

        if (incident is None):
            return {
                "message": "Incident id {} not found!".format(_id)
            }, 404

        addPageMetaData(incident)
        return incident_schema.dump(incident), 200


    @swagger.operation(notes="Delete incident by ID",
                       parameters=[
                           {
                               "name": "_id",
                               "description": "The Id of the incident",
                               "required": True,
                               "allowMultiple": False,
                               "dataType": "string",
                               "paramType": "path",
                           }
                       ],
                       responseMessages=[
                           {
                               "code": 200,
                               "message": "Incident deleted!"
                           },
                           {
                               "code": 404,
                               "message": "Incident not found"
                           }
                       ])
    # @login_required
    def delete(self, _id):
        incident = IncidentModel.find_by_id(_id)

        if not incident:
            return {
                "message": "Incident not found"
            }, 404

        incident.remove_from_db()

        return {
            "message": "Incident id {} deleted!".format(_id)
        }, 200


          
    @swagger.operation(notes="Update an Incident by id",
    parameters=[
            {
                "name": "incident",
                "description": "The Id of the incident",
                "required": True,
                "allowMultiple": False,
                "dataType": IncidentModelRequest.__name__,
                "paramType": "body",
            }
        ])
    # @login_required
    def put(self, _id):
            
            data = _incident_update_parser.parse_args()

            #check if organization exists in the database
            organization_record = OrganizationModel.find_by_id(data['organization'])
            if organization_record is None:
                return {'message': 'Organization id not found'}, 404

            #check if site exists in the database
            site_record = SiteModel.find_by_id(data['site'])
            if site_record is None:
                return {'message': 'Site id not found'}, 404

            reported_by_record = None
            if (data['reported_by']):
                #check if user who reported the incident exists
                reported_by_record = UserModel.find_by_id(data['reported_by'])
                if reported_by_record is None:
                    return {'message': 'User id not found'}, 404

            incident_type_record = None
            if (data['incident_type']):
                #check if incident type exists
                incident_type_record = IncidentTypeModel.find_by_id(data['incident_type'])
                if incident_type_record is None:
                    return {'message': 'Incident type not found'}, 404

            incident_status_record = None
            if (data['incident_status']):
                #check if incident type exists
                incident_status_record = IncidentStatusModel.find_by_id(data['incident_status'])
                if incident_status_record is None:
                    return {'message': 'Incident status not found'}, 404


            incident = IncidentModel.find_by_id(_id)

            if incident:
                incident.update_details(name = data['name'],
                               organization = organization_record,
                               site = site_record,
                               description =  data['description'],
                               reported_at = data['reported_at'],
                               discovered_at =  data['discovered_at'],
                               resolved_at =  data['resolved_at'],
                               occured_at =  data['occured_at'],
                               affected =  data['affected'],
                               reported_by =  reported_by_record,
                               incident_type = incident_type_record,
                               incident_status = incident_status_record,
                               updated_at = datetime.utcnow(),)

                addPageMetaData(incident)

                return incident_schema.dump(incident), 200

            return {'message': 'Audit not found'}, 404

