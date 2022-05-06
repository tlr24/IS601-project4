from flask_wtf import FlaskForm
from wtforms.fields import *

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()