from app.database.ma import ma
from app.models.audit import AuditModel
from app.schemas.act import ActSchemaMinimal
from app.schemas.organization import OrganizationSchemaMinimal
from app.schemas.answer import answers_schema_minimal, answers_schema
from app.schemas.site import SiteSchemaMinimal
from app.schemas.user import users_schema
from marshmallow import fields


class AuditSchemaMinimal(ma.SQLAlchemySchema):
    class Meta:
        model = AuditModel

    id = ma.auto_field()
    name = ma.auto_field()
    taken = ma.auto_field()
    organization = ma.auto_field()
    site = ma.auto_field()
    assigned = ma.auto_field()
    active = ma.auto_field()
    finalized = ma.auto_field()
    act = ma.Nested(ActSchemaMinimal)
    organization = ma.Nested(OrganizationSchemaMinimal)
    site = ma.Nested(SiteSchemaMinimal)
    answers = fields.Method("get_answers")

    def get_answers(self, obj):
        if hasattr(obj, "answers"):
            if type(self).__name__ == 'AuditSchemaMinimal':
                return answers_schema_minimal.dump(obj.answers)
            return answers_schema.dump(obj.answers)
        return None


class AuditCounter(AuditSchemaMinimal):
    id = ma.auto_field()
    name = ma.auto_field()
    

class AuditSchema(AuditSchemaMinimal):
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

    # #Meta fields for loading dropdowns
    _users = fields.Method("get_users")
    
    def get_users(self, obj):
        if hasattr(obj, "users"):
            return users_schema.dump(obj.users)
        return None


audit_schema_minimal = AuditSchemaMinimal()
audits_schema_minimal = AuditSchemaMinimal(many=True)

audit_schema = AuditSchema()
audits_schema = AuditSchema(many=True)

audit_counter = AuditCounter()
audits_counter = AuditCounter(many=True)