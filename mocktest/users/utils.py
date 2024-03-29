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
    if current_user.image_file=='male.png' or current_user.image_file=='female.png' or current_user.image_file=='other.png':       
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_name = random_hex + f_ext
    else:
        _, f_ext = os.path.splitext(form_picture.filename)
        try:
            os.remove(os.path.join(current_app.root_path, 'static', 'profile_pics', current_user.image_file))
            picture_name = os.path.splitext(current_user.image_file)[0] + "a" + f_ext
            picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics/', picture_name)
        except:
            pass
        picture_name = os.path.splitext(current_user.image_file)[0] + "a" + f_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'profile_pics/', picture_name)
    try:
        image = Image.open(form_picture)
        image.thumbnail((250,250))
        image.save(picture_path)
        success = True
    except:
        success = False
    return picture_name, success

def send_reset_email(user):
    sender_email = 'webacademyuserhelp@gmail.com'
    receiver_email = user.email
    password = 'Webacademy2021'
    token = user.get_reset_token()
    message = MIMEMultipart("alternative")
    message["Subject"] = "About Password Reset"
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
                <p style="background-color:white;color:black;border-radius:5px">Copy paste this in your browser <br/>{url_for('users.reset_token', token=token, _external=True)}</p>
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