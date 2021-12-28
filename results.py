import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def prepare_results(market_index, stock):
    tickers = [market_index, stock]
    df = yf.download(tickers=tickers, interval='1mo', period='5y')['Adj Close']

    # Beta number
    beta = calculate_beta_number(df, market_index, stock)

    # adjusted close price table
    df.index = pd.to_datetime(df.index).date
    records = df.to_records(index=True)
    adj_close_prices_with_date = list(records)

    return adj_close_prices_with_date, beta


def calculate_beta_number(adj_close_value_data_frame, market_index, stock):
    # Convert historical stock prices to daily percent change
    price_change = adj_close_value_data_frame.pct_change()

    # Deletes row one containing the NaN
    price_change = price_change.drop(price_change.index[0])

    # Create arrays for x and y variables in the regression model
    x = np.array(price_change[market_index]).reshape((-1, 1))
    y = np.array(price_change[stock])

    # Set up the model and define the type of regression
    model = LinearRegression().fit(x, y)

    return round(model.coef_[0], 2)