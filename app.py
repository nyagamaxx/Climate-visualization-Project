
# app.py
# Author: Maxwell Nyaga
# Project: Climate Change Data Visualization Platform (Streamlit + Matplotlib)
# Description: Streamlit web app that visualizes global temperature trends using Matplotlib.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Climate Change Visualizer", layout="wide")

st.title("🌍 Climate Change Data Visualization (Streamlit)")
st.markdown("Interactive dashboard built with Streamlit and Matplotlib. Upload the dataset `GlobalLandTemperaturesByCountry.csv` into the `/data` folder or use the uploader in the sidebar.")

@st.cache_data
def load_data(path='data/GlobalLandTemperaturesByCountry.csv'):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        return None
    df['dt'] = pd.to_datetime(df['dt'], errors='coerce')
    df = df.dropna(subset=['dt', 'AverageTemperature'])
    df = df.rename(columns={'AverageTemperature': 'Temp'})
    df['year'] = df['dt'].dt.year
    return df

df = load_data()

if df is None:
    st.warning("""Dataset not found. Please download **GlobalLandTemperaturesByCountry.csv** from Kaggle:
https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data
and place it in the `data/` folder, or upload a CSV file using the sidebar.""")
    uploaded = st.sidebar.file_uploader("Or upload a CSV file", type=['csv'])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        df['dt'] = pd.to_datetime(df['dt'], errors='coerce')
        df = df.dropna(subset=['dt', 'AverageTemperature'])
        df = df.rename(columns={'AverageTemperature': 'Temp'})
        df['year'] = df['dt'].dt.year

if df is not None:
    st.sidebar.header("Filters")
    countries = sorted(df['Country'].unique())
    default_countries = ['Kenya', 'United States', 'India']
    selected_countries = st.sidebar.multiselect("Select countries", countries, default=default_countries)

    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    year_range = st.sidebar.slider("Select year range", min_year, max_year, (1900, min(2013, max_year)))

    show_global = st.sidebar.checkbox("Show global average", value=True)
    normalize = st.sidebar.checkbox("Normalize zero-baseline (relative change)", value=False)
    smooth = st.sidebar.checkbox("Smooth lines (rolling mean)", value=False)
    window = st.sidebar.slider("Smoothing window (years)", 1, 21, 5) if smooth else 1

    filtered = df[(df['Country'].isin(selected_countries)) & (df['year'].between(year_range[0], year_range[1]))]

    st.subheader("📈 Temperature Trends")
    fig, ax = plt.subplots(figsize=(10,5))
    for country in selected_countries:
        sub = filtered[filtered['Country'] == country].groupby('year')['Temp'].mean().reset_index()
        if sub.empty:
            continue
        if smooth and window > 1:
            sub['Temp'] = sub['Temp'].rolling(window=window, center=True, min_periods=1).mean()
        if normalize:
            sub['Temp'] = sub['Temp'] - sub['Temp'].iloc[0]
        ax.plot(sub['year'], sub['Temp'], label=country)
    if show_global:
        global_avg = df[df['year'].between(year_range[0], year_range[1])].groupby('year')['Temp'].mean().reset_index()
        if smooth and window > 1:
            global_avg['Temp'] = global_avg['Temp'].rolling(window=window, center=True, min_periods=1).mean()
        if normalize:
            global_avg['Temp'] = global_avg['Temp'] - global_avg['Temp'].iloc[0]
        ax.plot(global_avg['year'], global_avg['Temp'], label='Global Avg', linewidth=2, color='black', linestyle='--')

    ax.set_title('Average Temperature Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Temperature (°C)' if not normalize else 'Temperature change (°C)')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    st.pyplot(fig)

    st.subheader('📊 Country Comparison (Average over selected range)')
    avg_df = filtered.groupby('Country')['Temp'].mean().reset_index().sort_values('Temp', ascending=True)
    fig2, ax2 = plt.subplots(figsize=(8,4))
    ax2.barh(avg_df['Country'], avg_df['Temp'])
    ax2.set_xlabel('Average Temperature (°C)')
    ax2.set_title('Average Temperature by Country (Selected Range)')
    st.pyplot(fig2)

    st.markdown('---')
    st.markdown('**Notes:** The dataset can be large. If the app runs slowly, consider uploading a smaller CSV or selecting fewer countries.')
