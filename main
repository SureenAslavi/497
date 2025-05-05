#%%writefile P5_Sureen_Aslavi.py
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
st.set_page_config(
    page_title="Gold Dashboard",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from google.colab import files
import numpy as np

df_reshaped = files.upload()

data = pd.read_csv(list(df_reshaped.keys())[0])
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m')


data['Year'] = data['Date'].dt.year


yearly_avg = data.groupby('Year')['Price'].mean().reset_index()


fig = px.line(
    yearly_avg,
    x='Year',
    y='Price',
    title='متوسط سعر الذهب السنوي',
    markers=True
)

st.plotly_chart(fig, use_container_width=True)
