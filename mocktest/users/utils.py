import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from mocktest import mail,app

def save_picture(form_picture):
    if current_user.image_file=='default.png':
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_name = random_hex + f_ext
    else:
        _, f_ext = os.path.splitext(form_picture.filename)
        try:
            os.remove(os.path.join(app.root_path, f'static/profile_pics/', current_user.image_file))
        except:
            pass
        picture_name = os.path.splitext(current_user.image_file)[0] + f_ext
    print(picture_name)
    picture_path = os.path.join(app.root_path, f'static/profile_pics/', picture_name)
    try:
        image = Image.open(form_picture)
        image.thumbnail((150,150))
        image.save(picture_path)
        success = True
    except:
        success = False
    return picture_name, success

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)