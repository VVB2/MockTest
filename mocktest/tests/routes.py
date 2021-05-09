import os
import time
from mocktest import db
from flask import (render_template,
                abort, Blueprint, jsonify, current_app as app, url_for, request, make_response, jsonify)
from mocktest.models import Java, Python, Marks
from flask_login import current_user, login_required
from  sqlalchemy.sql.expression import func

tests = Blueprint('tests', __name__)

@tests.route("/java-practice")
@login_required
def java():
    modules = ['Data_Types_Variables_Arrays','Operators_Control_Statements','Classes_Methods','Exception','Inheritance','Threads']
    counts = []

    for module in modules:
        counts.append(Java.query.filter_by(module=module).count())

    return render_template('java.html', title='Java MockTest Selection', image_file=current_user.image_file, module=counts)

@tests.route("/python-practice")
@login_required
def python():
    modules = ['Python_Basics','Strings','List','Loops','Tuples_Sets','Regular_Expression_Files']
    counts = []

    for module in modules:
        counts.append(Python.query.filter_by(module=module).count())

    return render_template('python.html', title='Python MockTest Selection', image_file=current_user.image_file, module=counts)

@tests.route("/<subject>/<module>", methods=['GET', 'POST'])
@login_required
def question(module, subject): 
    if request.method == 'POST':
        answers = request.get_json()
        score = 0

        for answer in answers:
            if (subject == 'java-question'):
                model_answer = Java.query.filter_by(id=int(answer)).first()
            else:
                model_answer = Python.query.filter_by(id=int(answer)).first()
            score += 2 if model_answer.answer == answers[answer] else 0

        marks_obj = Marks(subject=subject, module=module, marks_obtained=score, user_id=current_user.id)
        db.session.add(marks_obj)
        db.session.commit()

    else:
        if (subject == 'java-question'):
            data = Java.query.filter_by(module=module).order_by(func.random()).limit(20).all()
        else:     
            data = Python.query.filter_by(module=module).order_by(func.random()).limit(20).all()
        
        return render_template('questions.html', title=module.replace('_',' '), image_file=current_user.image_file, data=data
        , module=module, subject=subject)

    return render_template('futureUseCode.html', title=module.replace('_',' '), image_file=current_user.image_file, data=answers)
   
