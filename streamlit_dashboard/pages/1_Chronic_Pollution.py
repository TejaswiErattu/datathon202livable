"""
Page 1: Chronic Pollution Analysis
Top counties by Mean Median AQI (daily exposure burden)
Author: Tejaswi Erattutaj
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import re
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_shared_styles, page_header, section_label, section_divider

st.set_page_config(page_title="AirRisk - Chronic Pollution", page_icon="�", layout="wide")

# Apply shared CSS
apply_shared_styles(st)

# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.dirname(os.path.dirname(current_dir))
    
    file_paths = [
        os.path.join(data_dir, "annual_aqi_by_county_2021.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2022.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2023.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2024.csv"),
    ]
    
    df_list = []
    for file in file_paths:
        if os.path.exists(file):
            current_df = pd.read_csv(file)
            match = re.search(r'(\d{4})\.csv', file)
            if match:
                current_df['Year'] = int(match.group(1))
            df_list.append(current_df)
    
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()

@st.cache_data
def compute_county_stats(_df):
    """Compute aggregated county statistics - EXACT as in original notebook."""
    county_stats = _df.groupby(['State', 'County']).agg({
        'Median AQI': 'mean',
        'Max AQI': 'mean'
    }).reset_index()
    county_stats.columns = ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']
    return county_stats

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

county_stats = compute_county_stats(df)

# =============================================================================
# PAGE CONTENT
# =============================================================================
page_header(st, "Chronic Pollution Analysis", "Top Counties by Mean Median AQI (2021-2024)", "�")

st.markdown("""
<div class="callout-box">
<strong>What is Chronic Pollution?</strong> The Median AQI represents the <em>typical daily air quality</em> 
a resident experiences. A high average Median AQI over 4 years indicates persistent, day-in-day-out 
pollution exposure—the "daily grind" that affects long-term respiratory and cardiovascular health.
</div>
""", unsafe_allow_html=True)

section_divider(st)

# =============================================================================
# FILTERS
# =============================================================================
section_label(st, "Filters")

col1, col2 = st.columns(2)

with col1:
    states = ['All States'] + sorted(county_stats['State'].unique().tolist())
    selected_state = st.selectbox("Select State", states, key="chronic_state")

with col2:
    top_n = st.slider("Show Top N Counties", min_value=10, max_value=50, value=15, step=5, key="chronic_topn")

# Filter data
if selected_state != 'All States':
    filtered_stats = county_stats[county_stats['State'] == selected_state].copy()
else:
    filtered_stats = county_stats.copy()

# Get top N by chronic pollution (Mean Median AQI) - EXACT as notebook
chronic_top = filtered_stats.sort_values('mean_median_aqi', ascending=False).head(top_n)

section_divider(st)

# =============================================================================
# CHART - EXACT LOGIC FROM NOTEBOOK
# =============================================================================
section_label(st, f"Top {top_n} Counties by Chronic Pollution")

# Create horizontal bar chart like the original notebook
fig = px.bar(
    chronic_top.sort_values('mean_median_aqi', ascending=False),  # Highest at top
    x='mean_median_aqi',
    y='County',
    color='State',
    orientation='h',
    hover_data={
        'State': True,
        'mean_median_aqi': ':.1f',
        'mean_max_aqi': ':.1f'
    },
    labels={
        'mean_median_aqi': 'Average Median AQI (Daily Exposure)',
        'County': '',
        'State': 'State'
    },
    color_discrete_sequence=px.colors.sequential.Viridis
)

fig.update_layout(
    height=max(400, top_n * 28),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='white',
    font=dict(family="Inter, sans-serif", size=12),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        title=""
    ),
    margin=dict(l=20, r=20, t=60, b=40),
    xaxis_title="Average Median AQI (Daily Exposure)",
    yaxis_title=""
)

fig.update_xaxes(gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0')
fig.update_yaxes(gridcolor='#e2e8f0')

st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# INTERPRETATION
# =============================================================================
if len(chronic_top) > 0:
    worst_county = chronic_top.iloc[0]
    st.markdown(f"""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #2563eb; border-bottom: 1px solid #eff6ff; padding-bottom: 12px;">💡 What This Means</h4>
    <p><strong>{worst_county['County']}, {worst_county['State']}</strong> has the highest chronic pollution 
    burden with an average Median AQI of <strong>{worst_county['mean_median_aqi']:.1f}</strong> over 2021-2024.</p>
    <p style="margin-bottom: 0;">Counties with high Median AQI experience poor air quality as their <em>norm</em>—residents breathe 
    moderately unhealthy air on a typical day, leading to cumulative health impacts over time including 
    increased rates of asthma, cardiovascular disease, and reduced life expectancy.</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# DATA TABLE
# =============================================================================
with st.expander("📋 View Data Table"):
    display_df = chronic_top[['County', 'State', 'mean_median_aqi', 'mean_max_aqi']].copy()
    display_df.columns = ['County', 'State', 'Mean Median AQI', 'Mean Max AQI']
    display_df = display_df.round(1)
    display_df.index = range(1, len(display_df) + 1)
    st.dataframe(display_df, use_container_width=True)
