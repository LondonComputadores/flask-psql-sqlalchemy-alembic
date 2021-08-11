from app.database.ma import ma
from app.models.act import ActModel


class ActSchemaMinimal(ma.SQLAlchemySchema):
    class Meta:
        model = ActModel

    id = ma.auto_field()
    name = ma.auto_field()

class ActSchema(ActSchemaMinimal):
    class Meta:
        model = ActModel

    active = ma.auto_field()
    org_wide = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

act_schema_minimal = ActSchemaMinimal()
acts_schema_minimal = ActSchemaMinimal(many=True)

act_schema = ActSchema()
acts_schema = ActSchema(many=True)