from app.database.ma import ma
from app.models.incidents.incident import IncidentModel
from app.schemas.organization import OrganizationSchemaMinimal
from app.schemas.site import SiteSchemaMinimal, sites_schema_minimal
from app.schemas.user import UserSchema, users_schema
from app.schemas.incidents.incident_type import IncidentTypeSchema, incident_types_schema
from app.schemas.incidents.incident_status import IncidentStatusSchema, incident_status_schema
from marshmallow import fields

class IncidentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = IncidentModel
        ordered = True

    id = ma.auto_field()
    organization = ma.auto_field()
    name = ma.auto_field()
    site = ma.auto_field()
    description = ma.auto_field()
    reported_at = ma.auto_field()
    discovered_at = ma.auto_field()
    resolved_at = ma.auto_field()
    occured_at = ma.auto_field()
    affected = ma.auto_field()
    reported_by = ma.auto_field()
    incident_type = ma.auto_field()
    incident_status = ma.auto_field()
    active = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    organization = ma.Nested(OrganizationSchemaMinimal)
    site = ma.Nested(SiteSchemaMinimal)
    reported_by = ma.Nested(UserSchema)
    incident_type = ma.Nested(IncidentTypeSchema)
    incident_status = ma.Nested(IncidentStatusSchema)

    # #Meta fields for loading dropdowns
    _incident_types = fields.Method("get_incident_types")
    _incident_statuses = fields.Method("get_incident_statuses")
    _users = fields.Method("get_users")
    _sites = fields.Method("get_sites")

    def get_incident_types(self, obj):
        if hasattr(obj, "incident_types"):
            return incident_types_schema.dump(obj.incident_types)
        return None
    
    def get_incident_statuses(self, obj):
        if hasattr(obj, "incident_statuses"):
            return incident_status_schema.dump(obj.incident_statuses)
        return None

    def get_users(self, obj):
        if hasattr(obj, "users"):
            return users_schema.dump(obj.users)
        return None

    def get_sites(self, obj):
        if hasattr(obj, "sites"):
            return sites_schema_minimal.dump(obj.sites)
        return None


class IncidentCounter(IncidentSchema):
    id = ma.auto_field()
    name = ma.auto_field()


incident_schema = IncidentSchema()
incidents_schema = IncidentSchema(many=True)

incident_counter = IncidentCounter()
incidents_counter = IncidentCounter(many=True)