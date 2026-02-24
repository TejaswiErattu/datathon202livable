"""
Page 5: County Drilldown
Individual county profiles with yearly trends
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import re
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_shared_styles, page_header, section_label, section_divider

st.set_page_config(page_title="AirRisk - County Drilldown", page_icon="🔍", layout="wide")

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

def compute_county_stats(df):
    county_stats = df.groupby(['State', 'County']).agg({
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
page_header(st, "County Drilldown", "Explore Individual County Profiles", "🔍")

st.markdown("""
<div class="callout-box-teal">
<strong>Deep Dive:</strong> Select a specific county to view its air quality trends over 2021-2024, 
understand how it compares to thresholds, and download its data for further analysis.
</div>
""", unsafe_allow_html=True)

section_divider(st)

# =============================================================================
# COUNTY SELECTION
# =============================================================================
section_label(st, "Select County")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    states = sorted(df['State'].unique().tolist())
    selected_state = st.selectbox("Select State", states, key="drilldown_state")

with col2:
    counties_in_state = sorted(df[df['State'] == selected_state]['County'].unique().tolist())
    selected_county = st.selectbox("Select County", counties_in_state, key="drilldown_county")

with col3:
    percentile = st.slider(
        "Threshold Percentile", 
        min_value=80, max_value=99, value=90, step=1,
        help="Used to determine Double Jeopardy status"
    )

# =============================================================================
# COUNTY DATA
# =============================================================================
county_data = df[(df['State'] == selected_state) & (df['County'] == selected_county)].copy()
county_yearly = county_data.groupby('Year').agg({
    'Median AQI': 'mean',
    'Max AQI': 'mean',
    'Days with AQI': 'sum',
    'Good Days': 'sum',
    'Unhealthy Days': 'sum'
}).reset_index()

# Get county aggregated stats
county_agg = county_stats[(county_stats['State'] == selected_state) & 
                          (county_stats['County'] == selected_county)].iloc[0]

# Calculate thresholds for Double Jeopardy check
median_threshold = county_stats['mean_median_aqi'].quantile(percentile / 100)
max_threshold = county_stats['mean_max_aqi'].quantile(percentile / 100)

is_high_chronic = county_agg['mean_median_aqi'] >= median_threshold
is_high_acute = county_agg['mean_max_aqi'] >= max_threshold
is_double_jeopardy = is_high_chronic and is_high_acute

section_divider(st)

# =============================================================================
# COUNTY PROFILE
# =============================================================================
section_label(st, f"Profile: {selected_county}, {selected_state}")

# Metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "4-Year Mean Median AQI",
        f"{county_agg['mean_median_aqi']:.1f}",
        delta=f"{'Above' if is_high_chronic else 'Below'} {percentile}th %ile",
        delta_color="inverse" if is_high_chronic else "normal"
    )

with col2:
    st.metric(
        "4-Year Mean Max AQI",
        f"{county_agg['mean_max_aqi']:.1f}",
        delta=f"{'Above' if is_high_acute else 'Below'} {percentile}th %ile",
        delta_color="inverse" if is_high_acute else "normal"
    )

with col3:
    chronic_rank = (county_stats['mean_median_aqi'] >= county_agg['mean_median_aqi']).sum()
    st.metric(
        "Chronic Rank",
        f"#{chronic_rank}",
        delta=f"of {len(county_stats)} counties"
    )

with col4:
    acute_rank = (county_stats['mean_max_aqi'] >= county_agg['mean_max_aqi']).sum()
    st.metric(
        "Acute Rank",
        f"#{acute_rank}",
        delta=f"of {len(county_stats)} counties"
    )

# Double Jeopardy Status
if is_double_jeopardy:
    st.markdown(f"""
    <div class="warning-box">
    <h4 style="margin-top: 0; color: #c53030;">⚠️ DOUBLE JEOPARDY STATUS: YES</h4>
    <p>At the {percentile}th percentile threshold, <strong>{selected_county}</strong> qualifies as a 
    Double Jeopardy county. It exceeds both the chronic threshold ({median_threshold:.1f}) and 
    acute threshold ({max_threshold:.1f}).</p>
    </div>
    """, unsafe_allow_html=True)
else:
    status_text = []
    if is_high_chronic:
        status_text.append("High Chronic (above chronic threshold)")
    if is_high_acute:
        status_text.append("High Acute (above acute threshold)")
    if not status_text:
        status_text.append("Low Risk (below both thresholds)")
    
    st.markdown(f"""
    <div class="success-box">
    <h4 style="margin-top: 0; color: #38a169;">✓ DOUBLE JEOPARDY STATUS: NO</h4>
    <p>At the {percentile}th percentile threshold, <strong>{selected_county}</strong> does not qualify 
    as Double Jeopardy. Status: {', '.join(status_text)}.</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# YEARLY TREND CHART
# =============================================================================
st.markdown("### 📈 Yearly Trends (2021-2024)")

fig = make_subplots(rows=1, cols=2, subplot_titles=("Median AQI (Daily Exposure)", "Max AQI (Peak Events)"))

# Median AQI trend
fig.add_trace(
    go.Scatter(
        x=county_yearly['Year'],
        y=county_yearly['Median AQI'],
        mode='lines+markers',
        name='Median AQI',
        line=dict(color='#3182ce', width=3),
        marker=dict(size=10)
    ),
    row=1, col=1
)

# Add chronic threshold line
fig.add_hline(y=median_threshold, line_dash="dash", line_color="#dd6b20", 
              annotation_text=f"{percentile}th %ile Threshold", row=1, col=1)

# Max AQI trend
fig.add_trace(
    go.Scatter(
        x=county_yearly['Year'],
        y=county_yearly['Max AQI'],
        mode='lines+markers',
        name='Max AQI',
        line=dict(color='#c53030', width=3),
        marker=dict(size=10)
    ),
    row=1, col=2
)

# Add acute threshold line
fig.add_hline(y=max_threshold, line_dash="dash", line_color="#dd6b20", 
              annotation_text=f"{percentile}th %ile Threshold", row=1, col=2)

fig.update_layout(
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='white',
    font=dict(family="Inter, sans-serif", size=12),
    showlegend=False,
    margin=dict(l=20, r=20, t=60, b=40)
)

fig.update_xaxes(gridcolor='#e2e8f0', dtick=1)
fig.update_yaxes(gridcolor='#e2e8f0')

st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# INTERPRETATION
# =============================================================================
if len(county_yearly) > 1:
    median_trend = county_yearly['Median AQI'].iloc[-1] - county_yearly['Median AQI'].iloc[0]
    max_trend = county_yearly['Max AQI'].iloc[-1] - county_yearly['Max AQI'].iloc[0]
    
    median_direction = "improving" if median_trend < 0 else "worsening"
    max_direction = "improving" if max_trend < 0 else "worsening"
    
    st.markdown(f"""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #0f766e; border-bottom: 1px solid #f0fdfa; padding-bottom: 12px;">📊 Trend Analysis</h4>
    <ul>
        <li><strong>Chronic (Median AQI):</strong> {median_direction} by {abs(median_trend):.1f} points 
        from {county_yearly['Year'].min()} to {county_yearly['Year'].max()}</li>
        <li><strong>Acute (Max AQI):</strong> {max_direction} by {abs(max_trend):.1f} points 
        from {county_yearly['Year'].min()} to {county_yearly['Year'].max()}</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

section_divider(st)

# =============================================================================
# DATA TABLE & DOWNLOAD
# =============================================================================
section_label(st, "Raw Data")

display_df = county_yearly.copy()
display_df.columns = ['Year', 'Median AQI', 'Max AQI', 'Days with AQI', 'Good Days', 'Unhealthy Days']
display_df = display_df.round(1)

st.dataframe(display_df, use_container_width=True)

# Download button
csv = county_data.to_csv(index=False)
st.download_button(
    label="📥 Download County Data (CSV)",
    data=csv,
    file_name=f"{selected_county}_{selected_state}_aqi_data.csv",
    mime="text/csv"
)
