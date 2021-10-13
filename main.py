#%% Import the relevant packages

import yfinance as yf
import streamlit as st
import numpy as np
import os

#%% Page layout

st.write('# **STOCK DATA FETCH APP** :chart_with_upwards_trend:  :moneybag:')
st.write('The aim of this app is, after giving the ticker, to fetch the data from '
'yhaoo finance and doing some plot and summary ')

#%% Fetching data function

@st.cache 
def fetch_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date, interval='1d')
    info = stock.info
    return data, info, stock

# %% Body of the web app

add_box = st.sidebar.selectbox('Select what to get', ('-', 'Time Series', 'Key Values' , 'Financials', 'Save the data'))

ticker = st.text_input('Insert the ticker: ')
start_date = st.text_input('Insert the starting date as yyyy-mm-dd: ')
end_date = st.text_input('Insert the ending date as yyyy-mm-dd: ')
if not end_date:
    st.stop()

data, info, stock = fetch_data(ticker, start_date, end_date) # get the data


if add_box == 'Time Series': # part for the time series of variables

    dim = st.selectbox('Pick the financial measure needed', options=['-', 'Price', 'Return', 'Volume']) 
    
    if dim == 'Price':
        p = data.Close
        p.name='Adjusted Price'
        st.write('### Closing price adjusted for dividends and capital operations')
        st.line_chart(p)
    elif dim == 'Return':
        if st.checkbox('Arithmetic Return'):
            r = data.Close.pct_change()
            st.write('### Arithmetic return on adjusted price')
            r.name='Simple Return'
            st.line_chart(r)
        if st.checkbox('Log Return'):
            r = np.log(1 + data.Close.pct_change())
            st.write('### Logarithmic return on adjusted price')
            r.name = 'Log Return'
            st.line_chart(r)
    elif dim == 'Volume':
        st.write('### Stock trading volume')
        st.area_chart(data.Volume)
    
elif add_box == 'Key Values': # part for the key financial indicators
    st.write('### Financial indicators referring to the last fiscal year')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label='Return On Equity', value=str(np.round(info['returnOnEquity'],2)))
    col2.metric(label='Return On Assets', value=str(np.round(info['returnOnAssets'],2)))
    col3.metric(label='Debt to Equity', value=str(np.round(info['debtToEquity'],2)))
    col4.metric(label='Revenue per Share', value=str(np.round(info['revenuePerShare'],2)))

    col5, col6, col7, col8 = st.columns(4)
    col5.metric(label='Quick Ratio', value=str(np.round(info['quickRatio'],2)))
    col6.metric(label='Forward EPS', value=str(np.round(info['forwardEps'],2)))
    col7.metric(label='Book Value', value=str(np.round(info['bookValue'],2)))
    col8.metric(label='Price to Book', value=str(np.round(info['priceToBook'],2)))

    col9, col10, col11, col12 = st.columns(4)
    col9.metric(label='Short Ratio', value=str(np.round(info['shortRatio'],2)))
    col10.metric(label='Beta', value=str(np.round(info['beta'],2)))
    col11.metric(label='Dividend Yield', value=str(np.round(info['dividendYield'],2)))
    col12.metric(label='Dividend Rate', value=str(np.round(info['dividendRate'],2)))

elif add_box == 'Financials': # part for the financial sheets data
    dc = st.radio('Choose the financial document needed', ('Balance Sheet', 'Income Statement' ,'Cash Flow Statement'))
    if dc == 'Balance Sheet':
        st.write('### Balance Sheet data in millions for the last three fiscal years')
        df = stock.balancesheet.apply(lambda x: np.round(x/1000000,2))
        st.dataframe(df)
    elif dc == 'Income Statement':
        st.write('### Income Statement data in millions for the last three fiscal years')
        df = stock.financials.astype(float)
        df = df.apply(lambda x: np.round(x/1000000, 2))
        st.dataframe(df)
    elif dc == 'Cash Flow Statement':
        st.write('### Cash Flow Statement data in millions for the last three fiscal years')
        df = stock.cashflow.apply(lambda x: np.round(x/1000000, 2))
        st.dataframe(df)

elif add_box == 'Save the data':
    if st.checkbox('Insert path'):
        path = st.text_input('Insert the path for saving: ')
    elif st.checkbox('Use current path'):
        path = os.getcwd()
        path = path.replace('\\', '/') + '/'
    if st.button('Save data as .csv'):
        data.to_csv(path + ticker + '_data.csv')
    elif st.button('Save data as .xlsx'):
        data.to_excel(path + ticker + '_data.xlsx')