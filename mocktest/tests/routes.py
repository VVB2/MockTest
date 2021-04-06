from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

tests = Blueprint('tests', __name__)

@tests.route("/java-practice")
@login_required
def java():
    if(current_user.is_authenticated):
        return render_template('java.html', title='Java MockTest Selection', image_file=current_user.image_file)
    else:
        return render_template('java.html', title='Java MockTest Selection')

@tests.route("/python-practice")
@login_required
def python():
    if(current_user.is_authenticated):
        return render_template('python.html', title='Python MockTest Selection', image_file=current_user.image_file)
    else:
        return render_template('python.html', title='Python MockTest Selection')