import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from wordcloud import WordCloud
import re
from collections import Counter

st.set_page_config(
    page_title="Gold Price & Mining Production Dashboard",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

st.title("📊 Gold Price & Mining Production Dashboard")

price_data_path = "monthly.csv"
production_data_path = "Gold-Mining-Production-Volumes-Data-2024.xlsx"

col = st.columns((4,5,2), gap='medium')
    
with col[0]:   
    try:
        use_data_path = "gold_use.csv"
        use_data = pd.read_csv(use_data_path)
    
        if 'Category' in use_data.columns and 'Amount' in use_data.columns:
            use_data = use_data.sort_values(by='Amount', ascending=False)
            st.subheader("📊Gold Usage by Sector")
            use_fig = px.bar(
            use_data,
            x='Category',
            y='Amount',
            labels={'Amount': 'Gold Use (Tonnes)', 'Category': 'Sector'},
            color='Category',  
            color_discrete_sequence=px.colors.qualitative.Set2  
            )
        
            use_fig.update_layout(
                xaxis=dict(tickangle=0,tickfont=dict(size=11)),  
                legend_title_text='Sector'  
            )
        
            st.plotly_chart(use_fig, use_container_width=True)

        else:
            st.error("❌ 'gold_use.xlsx' must contain 'Category' and 'Amount' columns.")
    except FileNotFoundError:
        st.error(f"❌ File '{use_data_path}' not found. Please make sure it's in the same folder as main.py.")
    except Exception as e:
        st.error(f"An error occurred while processing Gold Usage data: {e}")


  

    st.subheader("🔥 Gold Investment Heatmap by Region and Year")

    investment_data_path = "Gold_Investment_Statistics_Dataset.csv"
    
    try:
        investment_df = pd.read_csv(investment_data_path)
        
        if 'Region' in investment_df.columns and 'Year' in investment_df.columns and 'Investment_Volume_Million_USD' in investment_df.columns:
            heatmap_data = investment_df.pivot(index='Region', columns='Year', values='Investment_Volume_Million_USD')
            heatmap_data.columns = heatmap_data.columns.astype(str)  

            fig = px.imshow(
                heatmap_data,
                labels=dict(x="Year", y="Region", color="Investment Volume (Million USD)"),
                x=heatmap_data.columns,
                y=heatmap_data.index,
                color_continuous_scale='YlOrRd',  
                aspect="auto",
            )
            
            fig.update_xaxes(
                tickmode='array',
                tickvals=heatmap_data.columns,  
                ticktext=heatmap_data.columns,  
                tickangle=0, 
                tickfont=dict(size=10)  
            )
            
            fig.update_layout(
                margin=dict(l=50, r=50, b=100, t=50),  
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
  
with col[1]:

    st.subheader("☁️ Word Cloud of Headlines by Country")
    
    news_data_path = "Gold_News_Headlines_Dataset.csv"
    
    basic_stopwords = set([
        "the", "is", "in", "and", "to", "of", "this", "that", "it", "on", "for",
        "with", "as", "its", "was", "but", "are", "have", "not", "you", "i"
    ])
    
    def clean_text(text, country):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'\b' + re.escape(country.lower()) + r'\b', '', text)
        return text
    
    try:
        news_data = pd.read_csv(news_data_path)
    
        if 'Country' in news_data.columns and 'Headline' in news_data.columns:
            countries = sorted(news_data['Country'].dropna().unique())
            selected_country = st.selectbox("Select a country:", countries)
    
            filtered_news = news_data[news_data['Country'] == selected_country]
            text = " ".join(filtered_news['Headline'].astype(str))
            cleaned_text = clean_text(text, selected_country)
    
            if cleaned_text.strip():
                tokens = cleaned_text.split()
                tokens = [word for word in tokens if word not in basic_stopwords and len(word) > 1]
                word_freq = Counter(tokens)
    
                wordcloud = WordCloud(
                    width=1000,
                    height=500,
                    background_color='white',
                    colormap='plasma'
                ).generate_from_frequencies(word_freq)
    
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                ax.set_title(f"Gold Market News Word Cloud - {selected_country}", fontsize=20, fontweight='bold')
                st.pyplot(fig)
            else:
                st.warning("No valid text to generate a word cloud for this country.")
        else:
            st.error("❌ The CSV must contain 'Country' and 'Headline' columns.")
    except FileNotFoundError:
        st.error(f"❌ File '{news_data_path}' not found.")
    except Exception as e:
        st.error(f"⚠️ An error occurred: {e}")
     
    gold_reserves_file = "World_official_gold_holdings_as_of_May2025.csv"  
    
   

    try:
        df_gold_reserves = pd.read_csv(gold_reserves_file)  
        df_gold_reserves.columns = df_gold_reserves.columns.str.strip()
    
        if {'Country', 'Tonnes'}.issubset(df_gold_reserves.columns):
            fig = px.choropleth(
                df_gold_reserves,
                locations="Country",
                locationmode="country names",
                color="Tonnes",
                hover_name="Country",
                hover_data=["Tonnes"],
                color_continuous_scale="YlOrRd",
                range_color=(0, df_gold_reserves["Tonnes"].max()),  
                labels={"Tonnes": "Gold Reserves (Tonnes)"}
            )
    
            fig.update_geos(
                projection_type="natural earth",
                showcountries=True,
                showframe=False,
                landcolor="lightgray",
                subunitcolor="white",
                fitbounds="locations"
            )
    
            fig.update_layout(
                margin=dict(l=0, r=0, t=4, b=0),  
                coloraxis_colorbar=dict(
                    thickness=15,
                    len=0.5,
                    title_side="right"
                )
            )
    
            st.subheader("🌎 Gold Reserves by Country")

            st.plotly_chart(
                fig, 
                use_container_width=True,
                config={'displayModeBar': False}
            )
                
        else:
            st.error("❌ CSV must contain 'Country' and 'Tonnes' columns")
    
    except FileNotFoundError:
        st.error("❌ File not found. Please check 'gold_reserves.csv' exists")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")



with col[2]:

    try:
        price_data = pd.read_csv(price_data_path)
    
        if 'Date' in price_data.columns and 'Price' in price_data.columns:
            price_data['Date'] = pd.to_datetime(price_data['Date'], format='%Y-%m', errors='coerce')
            price_data = price_data.dropna(subset=['Date'])
            st.subheader("📈Average Annual Gold Price")

            price_data['Year'] = price_data['Date'].dt.year
    
            yearly_avg_price = price_data.groupby('Year')['Price'].mean().reset_index()
    
            current_year = datetime.now().year
    
            last_20_years_price = yearly_avg_price[yearly_avg_price['Year'] >= (current_year - 20)]
    
            price_fig = px.line(
                last_20_years_price,
                x='Year',
                y='Price',
                markers=True
            )
    
            st.plotly_chart(price_fig, use_container_width=True)
        else:
            st.error("❌ 'monthly.csv' must contain 'Date' and 'Price' columns.")
    except FileNotFoundError:
        st.error(f"❌ File '{price_data_path}' not found. Please make sure it's in the same folder as main.py.")
    except Exception as e:
        st.error(f"An error occurred while processing Gold Price data: {e}")
