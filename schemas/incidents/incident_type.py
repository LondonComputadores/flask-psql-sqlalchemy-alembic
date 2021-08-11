from app.database.ma import ma
from app.models.incidents.incident_type import IncidentTypeModel

class IncidentTypeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = IncidentTypeModel
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    # active = ma.auto_field()
    # created_at = ma.auto_field()
    # updated_at = ma.auto_field()




incident_type_schema = IncidentTypeSchema()
incident_types_schema = IncidentTypeSchema(many=True)