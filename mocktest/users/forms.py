import phonenumbers
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from mocktest.models import User
from wtforms import (BooleanField, PasswordField, RadioField, StringField,
                     SubmitField, SelectMultipleField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    gender = RadioField('Gender', validators=[DataRequired()], choices=['Male','Female','Others'])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email already exists!')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountUpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "Enter your username"})
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])    
    phoneno = StringField('Contact No', render_kw={"placeholder": "Enter your contact no"})  
    address = StringField('Enter Your Address',render_kw={"placeholder": "Enter your address"})  
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username already taken!')
    
    def validate_phoneno(self, phoneno):
        if phoneno.data:
            if phoneno.data != current_user.phoneno:
                user = User.query.filter_by(phoneno = phoneno.data).first()
                if user:
                    raise ValidationError('Contact no already in use!')
            try:
                p = phonenumbers.parse(phoneno.data,"IN")
                if not phonenumbers.is_valid_number(p):
                    raise ValueError()
            except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
                raise ValidationError('Please enter a valid contact no!')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if not user:
            raise ValidationError('There is no account with that email. You must register first')

class ResetPasswordForm(FlaskForm):
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Reset Password')
