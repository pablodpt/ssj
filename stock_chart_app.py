import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ta.trend import SMAIndicator, EMAIndicator

def fetch_stock_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

def calculate_indicators(df):
    df['SMA20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
    df['SMA50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
    df['SMA200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()
    df['EMA9'] = EMAIndicator(close=df['Close'], window=9).ema_indicator()
    return df

def create_chart(df):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                        row_heights=[0.7, 0.3])

    # Candlestick chart
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'], name='Candlesticks'),
                  row=1, col=1)

    # Add moving averages and EMA
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], name='SMA20', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], name='SMA50', line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA200'], name='SMA200', line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA9'], name='EMA9', line=dict(color='purple')), row=1, col=1)

    # Volume chart
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume'), row=2, col=1)

    fig.update_layout(title='Interactive Stock Chart', xaxis_rangeslider_visible=False, height=800, width=1200)
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])

    return fig

def main():
    st.set_page_config(layout="wide")
    st.title("Interactive Stock Chart")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        ticker = st.text_input("Enter stock ticker (e.g., AAPL):", value="AAPL")

    with col2:
        start_date = st.date_input("Start date")

    with col3:
        end_date = st.date_input("End date")

    if st.button("Generate Chart"):
        df = fetch_stock_data(ticker, start_date, end_date)
        df = calculate_indicators(df)
        fig = create_chart(df)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
