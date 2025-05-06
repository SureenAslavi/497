import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from wordcloud import WordCloud

# Streamlit page configuration
st.set_page_config(
    page_title="Gold Price & Mining Production Dashboard",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable dark theme for Altair
alt.themes.enable("dark")

# App title
st.title("📊 Gold Price & Mining Production Dashboard")

# Load CSV files directly from the project folder
price_data_path = "monthly.csv"
production_data_path = "Gold-Mining-Production-Volumes-Data-2024.xlsx"

col = st.columns((2, 4.5, 2), gap='medium')
with col[0]:
# Load and process Gold Price data
    try:
        price_data = pd.read_csv(price_data_path)
    
        # Check for required columns
        if 'Date' in price_data.columns and 'Price' in price_data.columns:
            # Convert 'Date' column to datetime
            price_data['Date'] = pd.to_datetime(price_data['Date'], format='%Y-%m', errors='coerce')
            price_data = price_data.dropna(subset=['Date'])
    
            # Extract year
            price_data['Year'] = price_data['Date'].dt.year
    
            # Calculate yearly average
            yearly_avg_price = price_data.groupby('Year')['Price'].mean().reset_index()
    
            # Get the current year
            current_year = datetime.now().year
    
            # Filter data for the last 20 years
            last_20_years_price = yearly_avg_price[yearly_avg_price['Year'] >= (current_year - 20)]
    
            # Plot Gold Price Chart
            price_fig = px.line(
                last_20_years_price,
                x='Year',
                y='Price',
                title='Average Annual Gold Price (Last 20 Years)',
                markers=True
            )
    
            st.plotly_chart(price_fig, use_container_width=True)
        else:
            st.error("❌ 'monthly.csv' must contain 'Date' and 'Price' columns.")
    except FileNotFoundError:
        st.error(f"❌ File '{price_data_path}' not found. Please make sure it's in the same folder as main.py.")
    except Exception as e:
        st.error(f"An error occurred while processing Gold Price data: {e}")
    # Load and process Gold Use data from Excel
    use_data_path = "gold_use.xlsx"
 
with col[2]:   
    try:
        use_data = pd.read_excel(use_data_path)
    
        if 'Category' in use_data.columns and 'Amount' in use_data.columns:
            #st.subheader("Gold Usage by Sector")
            # Sort the data by 'Amount' in descending order
            use_data = use_data.sort_values(by='Amount', ascending=False)
            # Create a line plot using Plotly
            use_fig = px.bar(
                use_data,
                x='Category',
                y='Amount',
                title='Gold Usage by Sector',
                labels={'Amount': 'Gold Use (Tonnes)', 'Category': 'Sector'},
                color='Amount',
                color_continuous_scale='sunset'
            )
    
            st.plotly_chart(use_fig, use_container_width=True)
        else:
            st.error("❌ 'gold_use.xlsx' must contain 'Category' and 'Amount' columns.")
    except FileNotFoundError:
        st.error(f"❌ File '{use_data_path}' not found. Please make sure it's in the same folder as main.py.")
    except Exception as e:
        st.error(f"An error occurred while processing Gold Usage data: {e}")
  
with col[1]:

    st.subheader("☁️ Word Cloud of Headlines by Country")
    
    news_data_path = "Gold_News_Headlines_Dataset.csv"
    
    try:
        news_data = pd.read_csv(news_data_path)
    
        if 'Country' in news_data.columns and 'Headline' in news_data.columns:
            countries = sorted(news_data['Country'].dropna().unique())
            selected_country = st.selectbox("Select a country:", countries)
    
            filtered_news = news_data[news_data['Country'] == selected_country]
            text = " ".join(filtered_news['Headline'].astype(str))
    
            if text.strip():
                wordcloud = WordCloud(
                    width=1000,
                    height=500,
                    background_color='white',
                    colormap='plasma'
                ).generate(text)
    
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.warning("No headlines available for this country.")
        else:
            st.error("❌ 'gold_news.csv' must contain 'Country' and 'Headline' columns.")
    except FileNotFoundError:
        st.error(f"❌ File '{news_data_path}' not found. Please make sure it's in the same folder as main.py.")
    except Exception as e:
        st.error(f"An error occurred while processing the news data: {e}")
