from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class ETFForm(FlaskForm):
    etf = StringField('ETF Ticket', validators=[DataRequired()])
    submit = SubmitField('Add')


class ComputeForm(FlaskForm):
    submit = SubmitField("Compute")