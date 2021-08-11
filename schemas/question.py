from app.database.ma import ma
from app.models.question import QuestionModel
from marshmallow import fields

class QuestionSchemaMinimal(ma.SQLAlchemySchema):
    class Meta:
        model = QuestionModel

    id = ma.auto_field()
    question = ma.auto_field()
    domain = ma.auto_field()


class QuestionSchema(QuestionSchemaMinimal):
    cmmc_ref = ma.auto_field()
    nist_ref = ma.auto_field()
    nist_score = ma.auto_field()
    coaching = ma.auto_field()

question_schema = QuestionSchemaMinimal()
questions_schema = QuestionSchemaMinimal(many=True)