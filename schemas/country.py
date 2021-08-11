from app.database.ma import ma
from app.models.country import CountryModel


class CountrySchemaMinimal(ma.SQLAlchemySchema):
    class Meta:
        model = CountryModel

    id = ma.auto_field()
    name = ma.auto_field()

class CountrySchema(CountrySchemaMinimal):
    class Meta:
        model = CountryModel

    active = ma.auto_field()
    code = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

country_schema_minimal = CountrySchemaMinimal()
countries_schema_minimal = CountrySchemaMinimal(many=True)

country_schema = CountrySchema()
countries_schema_minimal_schema = CountrySchema(many=True)