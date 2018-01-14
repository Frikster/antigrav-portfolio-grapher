from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import ETFForm, ComputeForm
import altair as alt
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

WIDTH = 600
HEIGHT = 300
list_data = [10, 20, 30, 20, 15, 30, 45]
list_name = ['l'+str(x) for x in range(1, 8, 1)]
df_list_old = pd.DataFrame({'data': list_data, 'name': list_name})

# Tickers to test: {'SDIV':25, 'DIV':25, 'ECH':50}




def fn(tickets):
    if sum(list(tickets.values())) != 100:
        return None

    datas = []
    cumulative_dividend = 0.0

    ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')

    for ticket in tickets:
        (data, meta_data) = ts.get_daily_adjusted(symbol=ticket, outputsize='full')
        cumulative_dividend += data["7. dividend amount"].sum()
        datas.append(data.drop(columns=["6. volume", "7. dividend amount", "8. split coefficient"]) *
                     (tickets[ticket]/100))
        print(cumulative_dividend)


    data = sum(datas).dropna(axis="rows", how="any")
    print("SUCCESS!")
    global df_list
    df_list = pd.DataFrame({"date": list(data["5. adjusted close"].keys()), "price": [k for k in data["5. adjusted close"]]})
    # return pd.DataFrame(data["5. adjusted close"])
    return pd.DataFrame({"date": list(data["5. adjusted close"].keys()), "price": [k for k in data["5. adjusted close"]]})
    # return data.to_json(orient="index")
# fn({'SDIV':100})




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    etfs = []
    initial_len = len(request.form)
    for i in range(initial_len-3):
        if request.form.get('etf'+str(i), None):
            etfs = etfs + [request.form['etf'+str(i)]]

    etf_form = ETFForm()
    compute_form = ComputeForm()
    if etf_form.validate_on_submit():
        new_etf = request.form['etf']
        etfs = etfs + [new_etf]


    if compute_form.validate_on_submit():
        split_even = 100 / len(etfs)
        tickets = dict(zip(etfs, [split_even] * len(etfs)))
        print("ABOUT TO COMPUTE!")
        print(tickets)
        p = fn(tickets)
        # df_list = p
        print(df_list)

    return render_template('base.html', form=etf_form, etfs=etfs)

        # return render_template('base.html', form=etf_form, etfs=etfs)  # todo: make different?

@app.route("/line")
def data_line():
    print("data_line")
    print(df_list)
    chart = alt.Chart(data=df_list, height=HEIGHT, width=WIDTH).mark_line().encode(
        x='date:T',
        y='price:Q',
    )
    return chart.to_json()

# @app.route('/handle_data', methods=['POST'])
# def handle_data():
#     new_etf = request.form['etf']
#     etfs = etfs + [new_etf]
#     print(new_etf)
#     # process etf
#     return
print("done")