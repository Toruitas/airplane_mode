__author__ = 'Stuart'

from flask.ext.wtf import Form
from wtforms import FloatField, StringField
from wtforms.validators import DataRequired

class DonateForm(Form):
    amount = FloatField("Amount ($USD)", validators=[DataRequired(message="Please enter a valid amount.")])
    email = StringField("Email", validators=[DataRequired(message="Please enter a valid email.")])