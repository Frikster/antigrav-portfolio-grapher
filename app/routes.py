from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import ETFForm
from altair import Chart, X, Y, Axis, Data, DataFormat
import pandas as pd

WIDTH = 600
HEIGHT = 300
list_data = [10, 20, 30, 20, 15, 30, 45]
list_name = ['l'+str(x) for x in range(1,8,1)]
df_list = pd.DataFrame({'data':list_data, 'name':list_name})


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    etfs = ["BLEH", "MEH", "HAHA"]
    form = ETFForm()
    if form.validate_on_submit():
        new_etf = request.form['etf']
        etfs = etfs + [new_etf]
        print(new_etf)
        return render_template('base.html', form=form, etfs=etfs) #todo: make different?
    return render_template('base.html', form=form, etfs=etfs)

@app.route("/line")
def data_line():
    chart = Chart(data=df_list, height=HEIGHT, width=WIDTH).mark_line().encode(
        X('name', axis=Axis(title='Sample')),
        Y('data', axis=Axis(title='Value'))
    )
    return chart.to_json()

# @app.route('/handle_data', methods=['POST'])
# def handle_data():
#     new_etf = request.form['etf']
#     etfs = etfs + [new_etf]
#     print(new_etf)
#     # process etf
#     return