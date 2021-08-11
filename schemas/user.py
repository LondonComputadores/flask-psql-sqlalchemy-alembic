from app.database.ma import ma
from app.models.user import UserModel
from app.schemas.country import CountrySchemaMinimal
from app.schemas.state import StateSchemaMinimal


class UserSchemaMinimal(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    id = ma.auto_field()
    email = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    active = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()


user_schema_minimal = UserSchemaMinimal()
users_schema_minimal = UserSchemaMinimal(many=True)


class UserCounter(UserSchemaMinimal):
    id = ma.auto_field()
    # name = ma.auto_field()


class UserSchema(UserSchemaMinimal):
    class Meta:
            model = UserModel

    phone = ma.auto_field()
    mobile = ma.auto_field()
    zip = ma.auto_field()
    city = ma.auto_field()
    country = ma.Nested(CountrySchemaMinimal)
    state = ma.Nested(StateSchemaMinimal)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_schema = UserCounter()
users_schema = UserCounter(many=True)