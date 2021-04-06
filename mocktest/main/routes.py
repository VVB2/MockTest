from flask import render_template, request, Blueprint
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if(current_user.is_authenticated):
        return render_template('base.html', image_file=current_user.image_file)
    else:
        return render_template('base.html')