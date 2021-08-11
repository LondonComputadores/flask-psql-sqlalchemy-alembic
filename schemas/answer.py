from app.database.ma import ma
from app.models.answer import AnswerModel
from app.schemas.question import QuestionSchema, QuestionSchemaMinimal
from app.schemas.user import UserSchema
from marshmallow import fields

class AnswerSchemaMinimal(ma.SQLAlchemySchema):
    class Meta:
        model = AnswerModel

    id = ma.auto_field()
    answer = fields.String()
    position = ma.auto_field()
    answer = fields.Method("get_answer")
    question = ma.Nested(QuestionSchemaMinimal)
    assigned = ma.Nested(UserSchema)

    def get_answer(self, obj):
        if hasattr(obj, "answer"):
            return obj.answer.value
        return None

class AnswerSchema(AnswerSchemaMinimal):
    notes = ma.auto_field()
    question = ma.Nested(QuestionSchema)
    explanation = ma.auto_field()
    
answer_schema_minimal = AnswerSchemaMinimal()
answers_schema_minimal = AnswerSchemaMinimal(many=True)

answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)