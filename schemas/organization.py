from app.database.ma import ma
from app.models.organization import OrganizationModel


class OrganizationSchemaMinimal(ma.SQLAlchemySchema):
    class Meta:
        model = OrganizationModel

    id = ma.auto_field()
    name = ma.auto_field()

class OrganizationSchema(OrganizationSchemaMinimal):

    address_1 = ma.auto_field()
    address_2 = ma.auto_field()
    active = ma.auto_field()
    zip = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()



organization_schema = OrganizationSchema()
organizations_schema = OrganizationSchema(many=True)