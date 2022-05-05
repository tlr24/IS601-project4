from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class register_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),

    ], description="You need to signup with an email address")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password")
    confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")
    submit = SubmitField()
