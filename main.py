# %% Import the relevant packages

import yfinance as yf
import streamlit as st
import numpy as np
import os
from typing import Tuple
from pandas import DataFrame
import pandas as pd

# %% Page layout

st.write("# **STOCK DATA FETCH APP** :chart_with_upwards_trend:  :moneybag:")
st.write(
    "The aim of this app is, after giving the ticker, to fetch the data from "
    "yhaoo finance and doing some plots and summary "
)

# %% Fetching data function


@st.cache
def fetch_data(
    ticker: str, start_date: str, end_date: str
) -> Tuple[DataFrame, dict, object]:
    """Function to fetch the data according to the given Ticker

    Args:
        ticker (str): ticker of the stock to be fetched
        start_date (str): date from which start to fetch the data
        end_date (str): date from which ending the data fetching

    Returns:
        data: (DataFrame): data about the stock (e.g. Open, High, Low, Close, etc.)
        info: (dict): dictionary with many financial information about the company
        stock: (object): instance of the Ticker class
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, interval="1d")
    info = stock.info
    return data, info, stock


#%% Data conversion function


def convert_df(df: DataFrame):

    return df.to_csv(index=False).encode("utf-8")


# %% Body of the web app


add_box = st.sidebar.selectbox(
    "Select what to get",
    (
        "Insert Inputs",
        "Time Series",
        "Key Values",
        "Financials",
    ),
)

ticker = st.text_input("Insert the ticker: ")
start_date = st.text_input("Insert the starting date as yyyy-mm-dd: ")
end_date = st.text_input("Insert the ending date as yyyy-mm-dd: ")
if not end_date:
    st.stop()

data, info, stock = fetch_data(ticker, start_date, end_date)  # get the data


if add_box == "Time Series":  # part for the time series of variables

    data_dwn = convert_df(data)  # convert the dataframe to a csv

    st.download_button(
        label="Download data",
        data=data_dwn,
        file_name=f"{ticker}_data.csv",
        mime="text/csv",
        key="download-csv",
    )

    dim = st.selectbox(
        "Pick the financial measure needed", options=["-", "Price", "Return", "Volume"]
    )

    if dim == "Price":
        p = data.Close
        p.name = "Adjusted Price"
        st.write("### Closing price adjusted for dividends and capital operations")
        st.line_chart(p)
    elif dim == "Return":
        if st.checkbox("Arithmetic Return"):
            r = data.Close.pct_change()
            st.write("### Arithmetic return on adjusted price")
            r.name = "Simple Return"
            st.line_chart(r)
        if st.checkbox("Log Return"):
            r = np.log(1 + data.Close.pct_change())
            st.write("### Logarithmic return on adjusted price")
            r.name = "Log Return"
            st.line_chart(r)
    elif dim == "Volume":
        st.write("### Stock trading volume")
        st.area_chart(data.Volume)

elif add_box == "Key Values":  # part for the key financial indicators
    st.write("### Financial indicators referring to the last fiscal year")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        label="Return On Equity", value=str(np.round(info["returnOnEquity"], 2))
    )
    col2.metric(
        label="Return On Assets", value=str(np.round(info["returnOnAssets"], 2))
    )
    col3.metric(label="Debt to Equity", value=str(np.round(info["debtToEquity"], 2)))
    col4.metric(
        label="Revenue per Share", value=str(np.round(info["revenuePerShare"], 2))
    )

    col5, col6, col7, col8 = st.columns(4)
    col5.metric(label="Quick Ratio", value=str(np.round(info["quickRatio"], 2)))
    col6.metric(label="Forward EPS", value=str(np.round(info["forwardEps"], 2)))
    col7.metric(label="Book Value", value=str(np.round(info["bookValue"], 2)))
    col8.metric(label="Price to Book", value=str(np.round(info["priceToBook"], 2)))

    col9, col10, col11, col12 = st.columns(4)
    col9.metric(label="Short Ratio", value=str(np.round(info["shortRatio"], 2)))
    col10.metric(label="Beta", value=str(np.round(info["beta"], 2)))
    col11.metric(label="Dividend Yield", value=str(np.round(info["dividendYield"], 2)))
    col12.metric(label="Dividend Rate", value=str(np.round(info["dividendRate"], 2)))

elif add_box == "Financials":  # part for the financial sheets data
    dc = st.radio(
        "Choose the financial document needed",
        ("Balance Sheet", "Income Statement", "Cash Flow Statement"),
    )
    if dc == "Balance Sheet":
        st.write("### Balance Sheet data in millions for the last four fiscal years")
        df = stock.balancesheet.apply(
            lambda x: np.round(x / 1000000, 2)
        )  # round in millions
        df.columns = pd.to_datetime(df.columns).year  # convert the date to year unit
        st.dataframe(df)
    elif dc == "Income Statement":
        st.write("### Income Statement data in millions for the last four fiscal years")
        df = stock.financials.astype(float)
        df = df.apply(lambda x: np.round(x / 1000000, 2))  # round in millions
        df.columns = pd.to_datetime(df.columns).year  # convert the date to year unit
        st.dataframe(df)
    elif dc == "Cash Flow Statement":
        st.write(
            "### Cash Flow Statement data in millions for the last four fiscal years"
        )
        df = stock.cashflow.apply(
            lambda x: np.round(x / 1000000, 2)
        )  # round in millions
        df.columns = pd.to_datetime(df.columns).year  # convert the date to year unit
        st.dataframe(df)

# %% Change general appearance

hide_st_style = """
            <style>
            #MainMenu {visibiliy: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
