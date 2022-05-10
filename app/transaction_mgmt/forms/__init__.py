from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class add_transaction_form(FlaskForm):
    type = SelectField('Type', [
    ], description="Type of transaction", choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')])

    amount = IntegerField('Amount', [
        validators.DataRequired(),
    ], description="Integer amount of transaction")

    submit = SubmitField()