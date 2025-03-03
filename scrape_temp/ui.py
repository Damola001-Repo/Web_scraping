import streamlit as st
import plotly.express as px
import pandas as pd

data = pd.read_csv('scrape_temp/data.txt')


figure = px.line(x=data['date'].to_numpy(), y=data['temperature'].to_numpy(), labels={"x":"Date", "y":"Temperature"})
st.plotly_chart(figure)