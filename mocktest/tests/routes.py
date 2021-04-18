import os
from flask import (render_template,
                abort, Blueprint, json, current_app as app, url_for)
from flask_login import current_user, login_required

tests = Blueprint('tests', __name__)
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

@tests.route("/java-practice")
@login_required
def java():
    return render_template('java.html', title='Java MockTest Selection', image_file=current_user.image_file)

@tests.route("/python-practice")
@login_required
def python():
        return render_template('python.html', title='Python MockTest Selection', image_file=current_user.image_file)

@tests.route("/java-practice/<page>")
@login_required
def java_que(page):
    #filename = url_for('static', filename='questions/'+ page +'.json')
    filename = os.path.join(SITE_ROOT, 'static', 'questions', page +'.json')
    print(filename)
    with open(filename) as test_file:
        data = json.load(test_file)
    return render_template('java_questions.html', title='Java MockTest Selection', image_file=current_user.image_file, data=data)
