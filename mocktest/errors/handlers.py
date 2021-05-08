from flask import Blueprint, render_template
from flask_login import current_user

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    if current_user.is_authenticated:
        return render_template('errors/404.html', image_file=current_user.image_file), 404
    else:
        return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    if current_user.is_authenticated:
        return render_template('errors/403.html', image_file=current_user.image_file), 403
    else:
        return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    if current_user.is_authenticated:
        return render_template('errors/500.html', image_file=current_user.image_file), 500
    else:
        return render_template('errors/500.html'), 500