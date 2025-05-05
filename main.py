import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Streamlit page configuration
st.set_page_config(
    page_title="Gold Price Dashboard",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable dark theme for Altair
alt.themes.enable("dark")

# App title
st.title("📊 Gold Price Dashboard")

# Load CSV file directly from the project folder
DATA_PATH = "gold_data.csv"

try:
    data = pd.read_csv(DATA_PATH)

    # Check for required columns
    if 'Date' in data.columns and 'Price' in data.columns:
        # Convert 'Date' column to datetime
        data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m', errors='coerce')
        data = data.dropna(subset=['Date'])

        # Extract year
        data['Year'] = data['Date'].dt.year

        # Calculate yearly average
        yearly_avg = data.groupby('Year')['Price'].mean().reset_index()

        # Plot
        fig = px.line(
            yearly_avg,
            x='Year',
            y='Price',
            title='Average Annual Gold Price',
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ 'gold_data.csv' must contain 'Date' and 'Price' columns.")
except FileNotFoundError:
    st.error(f"❌ File '{DATA_PATH}' not found. Please make sure it's in the same folder as main.py.")
except Exception as e:
    st.error(f"An error occurred: {e}")
