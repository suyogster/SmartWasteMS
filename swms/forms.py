from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from swms.models import User


class RegistrationForm(FlaskForm):
    fullname = StringField('Fullname', validators=[
        DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', validators=[DataRequired()], choices=[('admin', 'Administrator'), ('user', 'Worker')])
    created_by = StringField('Created By')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])

    submit = SubmitField('Create User')

    def validate_fullname(self, fullname):
        user = User.query.filter_by(fullname=fullname.data).first()
        if user:
            raise ValidationError('The username is taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if (user):
            raise ValidationError('The email is already taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    fullname = StringField('Fullname', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_fullname(self, fullname):
        if fullname.data != current_user.fullname:
            user = User.query.filter_by(fullname=fullname.data).first()
            if (user):
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if (user):
                raise ValidationError('That email is taken.')


class DustbinCreateForm(FlaskForm):
    dustbinName = StringField('Dustbin Name', validators=[DataRequired(), Length(min=2, max=20)])
    ultrasonicStatus = IntegerField('Ultrasonic Status', validators=[DataRequired()])
    gasStatus = IntegerField('Gas Status', validators=[DataRequired()])
    location = IntegerField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit')

