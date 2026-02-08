"""
Page 4: Severity Score Analysis
Normalized combined metric from notebook
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

st.set_page_config(page_title="Severity Score", page_icon="📈", layout="wide")

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
# FILTERS (added at the top)
# =============================================================================
section_label(st, "Filters")

col1, col2, col3 = st.columns(3)

with col1:
    year_range = st.slider(
        "Year Range to Include", 
        min_value=2021, max_value=2024, value=(2021, 2024), step=1,
        help="Select which years of data to include in the analysis",
        key="severity_year_range"
    )

with col2:
    states = ['All States'] + sorted(county_stats['State'].unique().tolist())
    selected_state = st.selectbox("Filter by State", states, key="severity_state")

with col3:
    top_n = st.slider("Show Top N Counties", min_value=10, max_value=50, value=20, step=5, key="severity_topn")

# Apply year filter and recalculate county stats
year_min, year_max = year_range
df_filtered = df[(df['Year'] >= year_min) & (df['Year'] <= year_max)].copy()

# Recalculate county stats with filtered years
county_stats_filtered = df_filtered.groupby(['State', 'County']).agg({
    'Median AQI': 'mean',
    'Max AQI': 'mean'
}).reset_index()
county_stats_filtered.columns = ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']

# =============================================================================
# PAGE CONTENT
# =============================================================================
years_text = f"{year_min}-{year_max}" if year_min != year_max else str(year_min)
page_header(st, "Severity Score Analysis", f"Combined Pollution Burden Metric ({years_text})", "📈")

st.markdown("""
<div class="callout-box-purple">
<strong>What is the Severity Score?</strong> A single metric that combines both chronic and acute pollution 
exposure into one comparable number. It normalizes both dimensions to a 0-1 scale and averages them, 
allowing us to rank counties by overall pollution burden regardless of whether it's driven by daily 
exposure, extreme events, or both.
</div>
""", unsafe_allow_html=True)

section_divider(st)

# =============================================================================
# METHODOLOGY BOX
# =============================================================================
section_label(st, "How It's Calculated")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #9333ea; border-bottom: 1px solid #faf5ff; padding-bottom: 12px;">Normalization Formula</h4>
    <p>For each metric (Median AQI and Max AQI):</p>
    <pre style="background: #f8fafc; padding: 12px; border-radius: 8px; font-size: 0.85rem; border: 1px solid #e2e8f0;">
Normalized = (Value - Min) / (Max - Min)</pre>
    <p style="margin-bottom: 0;">This scales all values between 0 (best) and 1 (worst).</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #9333ea; border-bottom: 1px solid #faf5ff; padding-bottom: 12px;">Severity Score Formula</h4>
    <pre style="background: #f8fafc; padding: 12px; border-radius: 8px; font-size: 0.85rem; border: 1px solid #e2e8f0;">
Severity = (Norm_Median + Norm_Max) / 2</pre>
    <p style="margin-bottom: 0;">Equal weighting means a county with moderate chronic + moderate acute pollution 
    scores similarly to one with high chronic + low acute (or vice versa).</p>
    </div>
    """, unsafe_allow_html=True)

section_divider(st)

# =============================================================================
# DATA PROCESSING
# =============================================================================

# Filter data by state
if selected_state != 'All States':
    filtered_stats = county_stats_filtered[county_stats_filtered['State'] == selected_state].copy()
else:
    filtered_stats = county_stats_filtered.copy()

# Compute normalized scores and severity - using filtered data for normalization
stats_with_severity = filtered_stats.copy()
stats_with_severity['norm_median'] = (stats_with_severity['mean_median_aqi'] - stats_with_severity['mean_median_aqi'].min()) / \
                                     (stats_with_severity['mean_median_aqi'].max() - stats_with_severity['mean_median_aqi'].min())
stats_with_severity['norm_max'] = (stats_with_severity['mean_max_aqi'] - stats_with_severity['mean_max_aqi'].min()) / \
                                  (stats_with_severity['mean_max_aqi'].max() - stats_with_severity['mean_max_aqi'].min())
stats_with_severity['severity_score'] = (stats_with_severity['norm_median'] + stats_with_severity['norm_max']) / 2

# Get top N by severity
severity_top = stats_with_severity.sort_values('severity_score', ascending=False).head(top_n)

section_divider(st)

# =============================================================================
# CHART
# =============================================================================
section_label(st, f"Top {top_n} Counties by Severity Score")

fig = px.bar(
    severity_top.sort_values('severity_score', ascending=False),
    x='severity_score',
    y='County',
    color='State',
    orientation='h',
    hover_data={
        'State': True,
        'mean_median_aqi': ':.1f',
        'mean_max_aqi': ':.1f',
        'norm_median': ':.3f',
        'norm_max': ':.3f',
        'severity_score': ':.3f'
    },
    labels={
        'severity_score': 'Severity Score (0-1)',
        'County': '',
        'State': 'State',
        'norm_median': 'Normalized Chronic',
        'norm_max': 'Normalized Acute'
    },
    color_discrete_sequence=px.colors.sequential.Plasma
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
    xaxis_title="Severity Score (0 = Best, 1 = Worst)",
    yaxis_title="",
    xaxis_range=[0, 1]
)

fig.update_xaxes(gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0')
fig.update_yaxes(gridcolor='#e2e8f0')

st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# INTERPRETATION
# =============================================================================
if len(severity_top) > 0:
    worst_county = severity_top.iloc[0]
    st.markdown(f"""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #9333ea; border-bottom: 1px solid #faf5ff; padding-bottom: 12px;">💡 What This Means</h4>
    <p><strong>{worst_county['County']}, {worst_county['State']}</strong> has the highest Severity Score 
    of <strong>{worst_county['severity_score']:.3f}</strong> (on a 0-1 scale).</p>
    <p><strong>Component breakdown:</strong></p>
    <ul>
        <li>Normalized Chronic Score: {worst_county['norm_median']:.3f} (Mean Median AQI: {worst_county['mean_median_aqi']:.1f})</li>
        <li>Normalized Acute Score: {worst_county['norm_max']:.3f} (Mean Max AQI: {worst_county['mean_max_aqi']:.1f})</li>
    </ul>
    <p style="margin-bottom: 0;">A score close to 1.0 indicates a county near the worst on both dimensions. This metric helps 
    prioritize intervention by identifying counties with the highest <em>overall</em> pollution burden.</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# DATA TABLE
# =============================================================================
with st.expander("📋 View Full Data Table"):
    display_df = severity_top[['County', 'State', 'mean_median_aqi', 'mean_max_aqi', 
                               'norm_median', 'norm_max', 'severity_score']].copy()
    display_df.columns = ['County', 'State', 'Mean Median AQI', 'Mean Max AQI', 
                          'Norm. Chronic', 'Norm. Acute', 'Severity Score']
    display_df = display_df.round(3)
    display_df.index = range(1, len(display_df) + 1)
    st.dataframe(display_df, use_container_width=True)
