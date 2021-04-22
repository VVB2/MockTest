import os
import time
from flask import (render_template,
                abort, Blueprint, json, current_app as app, url_for)
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

@tests.route("/<subject>/<page>")
@login_required
def question(page, subject):
    if (subject == 'java-question'):
        data = Java.query.filter_by(module=page).all()
    else:
        if (page == 'Python_Basic'):
            page = page.replace('_', ' ')      
        data = Python.query.filter_by(module=page).all()
    return render_template('questions.html', title=page.replace('_',' '), image_file=current_user.image_file, data=data, page=page, subject=subject)
