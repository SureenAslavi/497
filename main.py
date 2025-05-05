import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

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
DATA_PATH = "monthly.csv"

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

        # Get the current year
        current_year = datetime.now().year

        # Filter data for the last 20 years
        last_20_years = yearly_avg[yearly_avg['Year'] >= (current_year - 20)]

        # Plot
        fig = px.line(
            last_20_years,
            x='Year',
            y='Price',
            title='Average Annual Gold Price (Last 20 Years)',
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ 'monthly.csv' must contain 'Date' and 'Price' columns.")
except FileNotFoundError:
    st.error(f"❌ File '{DATA_PATH}' not found. Please make sure it's in the same folder as main.py.")
except Exception as e:
    st.error(f"An error occurred: {e}")
