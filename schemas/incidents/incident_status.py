from app.database.ma import ma
from app.models.incidents.incident_status import IncidentStatusModel

class IncidentStatusSchema(ma.SQLAlchemySchema):
    class Meta:
        model = IncidentStatusModel
        ordered = True

    id = ma.auto_field()
    name = ma.auto_field()
    style = ma.auto_field()
    # active = ma.auto_field()
    # created_at = ma.auto_field()
    # updated_at = ma.auto_field()




incident_status_schema = IncidentStatusSchema()
incident_status_schema = IncidentStatusSchema(many=True)