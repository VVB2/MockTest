import os
import time
from flask import (render_template,
                abort, Blueprint, jsonify, current_app as app, url_for, request, make_response, json)
from mocktest.models import Java, Python
from flask_login import current_user, login_required

tests = Blueprint('tests', __name__)

@tests.route("/java-practice")
@login_required
def java():
    return render_template('java.html', title='Java MockTest Selection', image_file=current_user.image_file)

@tests.route("/python-practice")
@login_required
def python():
    return render_template('python.html', title='Python MockTest Selection', image_file=current_user.image_file)

@tests.route("/<subject>/<module>", methods=['GET', 'POST'])
@login_required
def question(module, subject):
    ROWS_PER_PAGE = 10	   
    if (subject == 'java-question'):
        page = request.args.get('page', 1, type=int)
        data = Java.query.filter_by(module=module).paginate(page=page, per_page=ROWS_PER_PAGE)
    else:
        if (module == 'Python_Basic'):
            module = module.replace('_', ' ')      
        page = request.args.get('page', 1, type=int)
        data = Python.query.filter_by(module=module).paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('questions.html', title=module.replace('_',' '), image_file=current_user.image_file, data=data, module=module, subject=subject)

@tests.route("/result", methods=['GET', 'POST'])
@login_required
def result_page(): 
    names = request.get_json()
    print(names)    
    return render_template('futureUseCode.html', data=names)
   
