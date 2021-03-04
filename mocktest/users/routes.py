from flask import render_template, url_for, flash, redirect, request, Blueprint, Markup
from flask_login import login_user, current_user, logout_user, login_required
from mocktest import db, bcrypt
from mocktest.models import User
from mocktest.users.forms import (RegistrationForm, LoginForm, AccountUpdateForm,
                                   RequestResetForm, ResetPasswordForm)
from mocktest.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(Markup(f'Login Successful! Welcome <strong>{ current_user.username }</strong>'), 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.username.data == current_user.username and form.phoneno.data == current_user.phoneno and form.address.data == current_user.address:
            return redirect(url_for('users.account'))
        current_user.username = form.username.data
        if form.picture.data:
            picture_file, picture_success = save_picture(form.picture.data) 
            if picture_success:
                current_user.image_file = picture_file
            else:
                flash('Error while updating profile picture', 'danger')   
        if form.phoneno.data:
            current_user.phoneno = form.phoneno.data
        if form.address.data:
            current_user.address = form.address.data
        db.session.commit()
        flash('Your account was successfully updated!', 'success')  
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        if not current_user.phoneno=='None':
            form.phoneno.data = current_user.phoneno
        if not current_user.address=='None':
            form.address.data = current_user.address
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form=form)

@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an expired or invalid token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
