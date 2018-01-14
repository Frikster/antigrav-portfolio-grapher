from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class ETFForm(FlaskForm):
    etf = StringField('ETF Ticket')
    submit = SubmitField('Add')