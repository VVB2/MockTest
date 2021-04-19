from flask_wtf import FlaskForm
from mocktest.models import Java
from wtforms import StringField, RadioField

class QuestionForm(FlaskForm):   
    print(FlaskForm.page)
    # questions = Java.query.filter_by(module=page).all()
    # for question in questions:
    #     print(question.module)
    #     question = StringField('question.question')
