from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd

class TicketError(Exception):
    pass

def fn(tickets):
    if sum(list(tickets.values())) != 100:
        return None

        datas = []
        cumulative_dividend = 0.0

        ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')

        for ticket in tickets:
            try:
                (data, meta_data) = ts.get_daily_adjusted(symbol=ticket, outputsize='full')
                cumulative_dividend += data["7. dividend amount"].sum()
                datas.append(data.drop(columns=["6. volume", "7. dividend amount", "8. split coefficient"]) *
                             (tickets[ticket]/100))
                # print(cumulative_dividend)
            except ValueError:
                raise TicketError(ticket)

        data = sum(datas).dropna(axis="rows", how="any")
        return data.to_json(orient="index")


if __name__ == "__main__":
    tickets = {'DDDD':25, 'DIV':25, 'ECH':50}

    print(fn(tickets))

# (data[~data["7. dividend amount"].isin([0.0000])])["7. dividend amount"].plot()
#print((data[~data["7. dividend amount"].isin([0.0000])])["7. dividend amount"].sum())
#print((data[~data["7. dividend amount"].isin([0.0000])])["7. dividend amount"])
# plt.title('Daily Times Series for the %s stock (Adjusted Close)' % ticket)
# plt.show()

# plot_json = fn(...) or plot_json
