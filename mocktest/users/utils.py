import smtplib, ssl
import os
import secrets
from PIL import Image
from flask import url_for, app, current_app
from flask_mail import Message
from mocktest import mail
from flask_login import current_user
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from dotenv import load_dotenv



def save_picture(form_picture):
    if current_user.image_file=='default.png':       
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_name = random_hex + f_ext
    else:
        _, f_ext = os.path.splitext(form_picture.filename)
        try:
            os.remove(os.path.join(current_app.root_path, 'static', 'profile_pics', current_user.image_file))
        except:
            pass
        picture_name = os.path.splitext(current_user.image_file)[0] + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics/', picture_name)
    try:
        image = Image.open(form_picture)
        image.thumbnail((150,150))
        image.save(picture_path)
        success = True
    except:
        success = False
    return picture_name, success

def send_reset_email(user):
    load_dotenv(current_app.root_path, '.env')
    sender_email = os.getenv('EMAIL_USER')
    receiver_email = user.email
    password = os.getenv('EMAIL_PASS')
    token = user.get_reset_token()
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
#     msg = Message('Password Reset Request',
#                   sender='noreply@gmail.com',
#                   recipients=[user.email])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('users.reset_token', token=token, _external=True)}
# If you did not make this request then simply ignore this email and no changes will be made.
# '''
#     mail.send(msg)
    html = f'''\
<!DOCTYPE html>
<html lang="en">
    <link href="http://steveville.org/assets/css/cosmo.css" rel="stylesheet" type="text/css" media="all" />
    <body>
        <div style="background-color:#1d1b1b;width:60%;margin:auto;color:#fff">
            <div style="padding:5px;background-color:#4285f4;border-bottom:0.5px solid #91a3b0">
                <h1 style="text-align:center;color:#1d1b1b">              
                    Web Academy
                </h1>
            </div>         
            <div style="text-align:center;font-weight:500;margin-top:10px">
                <h1>{user.username}, reset your password.</h1>
                <p style="color:#91a3b0">Looks like you forgot your password?</p>
                <p>
                    <strong>We're here to help. Click on the button below to reset your password.</strong>              
                </p>
                <p><button style="background-color:#1ca9c9;border-radius:5px;padding:10px;text-align:center;display:inline-block;font-size:16px;border:none"><a style="text-decoration:none;color:#fff" href="{url_for('users.reset_token', token=token, _external=True)}">Change my password</a></button></p>     
                <p style="margin-top:30px;padding-bottom:20px"><i>If you didn't ask to reset your password, please ignore this email.</i></p>
            </div>
        </div>
    </body>
</html>
'''
    html_part = MIMEText(html, "html")
    message.attach(html_part)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )