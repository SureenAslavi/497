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

col = st.columns((4, 4, 4), gap='medium')
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

    st.subheader("🔥 Gold Investment Heatmap by Region and Year")

    investment_data_path = "Gold_Investment_Statistics_Dataset.csv"
    
    try:
        investment_df = pd.read_csv(investment_data_path)
        
        if 'Region' in investment_df.columns and 'Year' in investment_df.columns and 'Investment_Volume_Million_USD' in investment_df.columns:
            # Create pivot table
            heatmap_data = investment_df.pivot(index='Region', columns='Year', values='Investment_Volume_Million_USD')
            heatmap_data.columns = heatmap_data.columns.astype(str)  # Convert years to strings
            
            # Create heatmap
            fig = px.imshow(
                heatmap_data,
                labels=dict(x="Year", y="Region", color="Investment Volume (Million USD)"),
                x=heatmap_data.columns,
                y=heatmap_data.index,
                color_continuous_scale='YlOrRd',  # Gold-appropriate color scale
                aspect="auto",
                title='Gold Investment Volume by Region and Year (Million USD)'
            )
            
            # Customize x-axis to show ALL years
            fig.update_xaxes(
                tickmode='array',
                tickvals=heatmap_data.columns,  # All years as values
                ticktext=heatmap_data.columns,  # All years as labels
                tickangle=0, 
                tickfont=dict(size=10)  # Adjust font size if needed
            )
            
            # Improve layout
            fig.update_layout(
                margin=dict(l=50, r=50, b=100, t=50),  # Adjust margins
                xaxis_title="Year",
                yaxis_title="Region",
                coloraxis_colorbar=dict(title="USD (Millions)")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.error("❌ CSV file must contain 'Region', 'Year', and 'Investment_Volume_Million_USD' columns.")
    except FileNotFoundError:
        st.error("❌ CSV file not found. Please ensure it's in your project directory.")
    except Exception as e:
        st.error(f"An error occurred while generating the heatmap: {e}")
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

    gold_reserves_file = "World_official_gold_holdings_as_of_May2025.csv"  # Make sure the CSV file path is correct
    
    # Streamlit app
    st.title("📊 Gold Reserves by Country")

    try:
        df_gold_reserves = pd.read_csv(gold_reserves_file)
        df_gold_reserves.columns = df_gold_reserves.columns.str.strip()  # Clean column names
    
        if 'Country' in df_gold_reserves.columns and 'Tonnes' in df_gold_reserves.columns:
            fig_gold_reserves = px.choropleth(
                df_gold_reserves, 
                locations="Country", 
                locationmode="country names",  
                color="Tonnes", 
                hover_name="Country", 
                hover_data=["Tonnes"],
                color_continuous_scale="YlOrRd",
                labels={"Tonnes": "Gold Reserves (Tonnes)"},
                title="Gold Reserves by Country (Tonnes)",
                height=600  # <--- Larger map height (adjust as needed)
            )
            
            # Optional: Adjust map zoom/center (e.g., focus on a specific region)
            fig_gold_reserves.update_geos(
                projection_type="natural earth",  # More global view
                # center=dict(lat=30, lon=0),  # Uncomment to center on a region
                # scope="asia"  # Uncomment to zoom to a continent
            )
            
            st.plotly_chart(fig_gold_reserves, use_container_width=True)  # Expands to container width
            
        else:
            st.error("❌ The CSV file must contain 'Country' and 'Tonnes' columns.")
    
    except FileNotFoundError:
        st.error(f"❌ File '{gold_reserves_file}' not found. Please check your directory.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
