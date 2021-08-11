from app.database.ma import ma
from app.models.site import SiteModel
from app.schemas.organization import OrganizationSchema

class SiteSchemaMinimal(ma.SQLAlchemySchema):
        class Meta:
            model = SiteModel

        id = ma.auto_field()
        name = ma.auto_field()

class SiteSchema(SiteSchemaMinimal):
    organization = ma.auto_field()
    address_1 = ma.auto_field()
    address_2 = ma.auto_field()
    city = ma.auto_field()
    state = ma.auto_field()
    country = ma.auto_field()
    zip = ma.auto_field()
    active = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    organization = ma.Nested(OrganizationSchema)




site_schema = SiteSchema()
sites_schema = SiteSchema(many=True)

site_schema_minimal = SiteSchemaMinimal();
sites_schema_minimal = SiteSchemaMinimal(many=True);