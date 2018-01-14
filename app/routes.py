from flask import render_template, flash, redirect, url_for
from app import app
import pandas as pd

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"