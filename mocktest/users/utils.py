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
    
    <body style="background-color: #ccc;align : center">
        <div class="text-center">
            <h1>               
                Web Academy
            </h1>
        </div>
        <hr>
        <br />
        <div class="maincontent" style="background-color: #FFF; margin: auto; padding: 20px; width: 450px; border-top: 2px solid #27ae60;">
            <div class="text-center">
                <h1>Dear {user.username},</h1>
                <p>Hello there future engineer!</p>
                <p>
                    Here is the link for password reset to your Web Academy account                 
                </p>
                <p><button><a class="btn btn-success btn-lg" href="{url_for('users.reset_token', token=token, _external=True)}"><i class="fa fa-check"></i>CHANGE PASSWORD</button></a></p>     
                <p>If the fancy button does not work, you can copy and paste this link into your browser:{url_for('users.reset_token', token=token, _external=True)}</p>
                <p>If this was not you please ignore this message.</p>
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