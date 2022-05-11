from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class add_user_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),

    ], description="Signup with email")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()

class edit_user_form(FlaskForm):
    about = TextAreaField('About', [validators.length(max=300)],
                          description="Add information about yourself")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()
