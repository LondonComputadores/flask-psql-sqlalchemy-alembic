from app.database.ma import ma
from app.models.state import StateModel


class StateSchemaMinimal(ma.SQLAlchemySchema):
    class Meta:
        model = StateModel

    id = ma.auto_field()
    name = ma.auto_field()

class StateSchema(StateSchemaMinimal):
    class Meta:
        model = StateModel

    active = ma.auto_field()
    code = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

state_schema_minimal = StateSchemaMinimal()
states_schema_minimal = StateSchemaMinimal(many=True)

state_schema = StateSchema()
states_schema_minimal_schema = StateSchema(many=True)