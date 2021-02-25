import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, Markup
from mocktest import app, db, bcrypt, mail
from mocktest.forms import RegistrationForm, LoginForm, AccountUpdateForm, RequestResetForm, ResetPasswordForm
from mocktest.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

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

@app.route("/")
def home():
    return render_template('base.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(Markup(f'Login Successful! Welcome <strong>{ current_user.username }</strong>'), 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
 
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        if form.picture.data:
            picture_file, picture_success = save_picture(form.picture.data) 
            if picture_success:
                current_user.image_file = picture_file
            else:
                flash('Error while updating profile picture', 'danger')  
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password  
        db.session.commit()
        flash('Your account was successfully updated!', 'success')  
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form=form)

@app.route("/java-practice")
@login_required
def java():
    return render_template('java.html', title='Java-Practice')

@app.route("/python-practice")
@login_required
def python():
    return render_template('python.html', title='Python-Practice')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an expired or invalid token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
