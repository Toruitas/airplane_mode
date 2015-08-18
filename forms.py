__author__ = 'Stuart'

from flask.ext.wtf import Form
from wtforms import FloatField, StringField
from wtforms.validators import DataRequired

class DonateForm(Form):
    amount = FloatField("Amount $", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])