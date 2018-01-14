from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import ETFForm
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

# Tickers to test: {'SDIV':25, 'DIV':25, 'ECH':25 'FBT}




def fn(tickets):
    if sum(list(tickets.values())) != 100:
        return None

    try:
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
    except:
        return None
    # return pd.DataFrame(data["5. adjusted close"])
    global df_list
    df_list = pd.DataFrame(
        {"date": list(data["5. adjusted close"].keys()), "price": [k for k in data["5. adjusted close"]]})
    return pd.DataFrame({"date": list(data["5. adjusted close"].keys()), "price": [k for k in data["5. adjusted close"]]})
    # return data.to_json(orient="index")
fn({'GOOGL':100})


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    etfs = []
    initial_len = len(request.form)
    print("LEN REQUEST.FORM")
    print(len(request.form))
    etf_form = ETFForm()

    if etf_form.submit_etf.data and etf_form.validate():
            prop = 100/(1+initial_len-3)

    for i in range(initial_len-3):
        if request.form.get('etf'+str(i), None):
            print("REACH HERE")
            new_etf = [request.form['etf'+str(i)], 100/(initial_len-3), 0, 0, 0, 0]
            etfs = etfs + [new_etf]

    # for i in range(initial_len-3):
    #     if request.form.get('etf'+str(i), None):
    #         print(request.form['etf' + str(i)])
    #         new_etf = [request.form['etf'+str(i)], 0, 0, 0, 0, 0]
    #         print("NEW_ETF")
    #         print(new_etf)
    #         etfs.append(new_etf)

    if etf_form.submit_etf.data and etf_form.validate():
        print("etf_form VALIDATED")
        new_etf = [request.form['etf'], 100/(1+len(etfs)), 0, 0, 0, 0]
        etfs = etfs + [new_etf]

        print("ETFS[0]")
        print(etfs[0])

        tickers = [e[0] for e in etfs]
        # proportions = [p[1] for p in etfs]
        proportions = [100/len(tickers) for p in etfs]

        tickets = dict(zip(tickers, proportions))
        print(tickets)
        p = fn(tickets)

    # compute_form = ComputeForm()
    # if compute_form.submit_compute.data and compute_form.validate():
    #     print("compute_form VALIDATED")
    #     split_even = 100 / len(etfs)
    #     tickets = dict(zip(etfs, [split_even] * len(etfs)))
    #     print("ABOUT TO COMPUTE!")
    #     print(tickets)
    #     p = fn(tickets)
        # df_list = p
        # print(df_list)

    print("ABOUT TO RENDER_TEMPLATE")
    return render_template('base.html', etf_form=etf_form, etfs=etfs)

        # return render_template('base.html', form=etf_form, etfs=etfs)  # todo: make different?

@app.route("/line")
def data_line():
    print("data_line")
    # try:
    #     print(df_list)
    # except NameError:
    #     df_list = df_list_old

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