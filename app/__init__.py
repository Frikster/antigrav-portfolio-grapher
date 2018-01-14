from flask import Flask, redirect
import dash
app_flask = Flask(__name__)
app_dash = dash.Dash()
# app_dash = dash.Dash(__name__, server=app_flask, url_base_pathname='/pathname')
from app import routes