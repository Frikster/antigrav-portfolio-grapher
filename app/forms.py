from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class ETFForm(FlaskForm):
    etf = StringField('ETF Ticket', validators=[DataRequired()])
    submit_etf = SubmitField('Add')


class ComputeForm(FlaskForm):
    submit_compute = SubmitField("Compute")