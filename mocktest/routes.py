import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, Markup
from mocktest import app, db, bcrypt
from mocktest.forms import RegistrationForm, LoginForm, AccountUpdateForm
from mocktest.models import User
from flask_login import login_user, current_user, logout_user, login_required

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
        image.thumbnail((200,200))
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
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            flash('Your password was updated', 'success')
        
        if picture_success:
            current_user.image_file = picture_file
            flash('Your account was successfully updated!', 'success')
        else:
            flash('Error while updating profile picture', 'danger')

        db.session.commit()
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