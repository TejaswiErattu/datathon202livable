"""
Page 2: Extreme Spikes Analysis
Top counties by Mean Max AQI (acute peak events)
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

st.set_page_config(page_title="AirRisk - Extreme Spikes", page_icon="⚡", layout="wide")

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
    """Compute aggregated county statistics - EXACT as in original notebook."""
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
page_header(st, "Extreme Pollution Spikes", "Top Counties by Mean Max AQI (2021-2024)", "⚡")

st.markdown("""
<div class="callout-box-orange">
<strong>What are Extreme Spikes?</strong> The Max AQI represents the <em>worst single day</em> of air quality 
each year. A high average Max AQI over 4 years indicates a county prone to dangerous pollution episodes—
from wildfires, industrial accidents, or severe inversions—that pose immediate health emergencies.
</div>
""", unsafe_allow_html=True)

section_divider(st)

# =============================================================================
# FILTERS
# =============================================================================
section_label(st, "Filters")

col1, col2, col3 = st.columns(3)

with col1:
    states = ['All States'] + sorted(county_stats['State'].unique().tolist())
    selected_state = st.selectbox("Select State", states, key="acute_state")

with col2:
    top_n = st.slider("Show Top N Counties", min_value=10, max_value=50, value=15, step=5, key="acute_topn")

with col3:
    outlier_handling = st.selectbox(
        "Outlier Handling",
        ["None", "Cap at 500", "Winsorize Top 1%"],
        help="Extreme Max AQI values (often from wildfires) can skew visualizations"
    )

# Filter data
if selected_state != 'All States':
    filtered_stats = county_stats[county_stats['State'] == selected_state].copy()
else:
    filtered_stats = county_stats.copy()

# Apply outlier handling
display_stats = filtered_stats.copy()
if outlier_handling == "Cap at 500":
    display_stats['mean_max_aqi_display'] = display_stats['mean_max_aqi'].clip(upper=500)
elif outlier_handling == "Winsorize Top 1%":
    p99 = display_stats['mean_max_aqi'].quantile(0.99)
    display_stats['mean_max_aqi_display'] = display_stats['mean_max_aqi'].clip(upper=p99)
else:
    display_stats['mean_max_aqi_display'] = display_stats['mean_max_aqi']

# Get top N by acute pollution (Mean Max AQI) - EXACT as notebook
acute_top = display_stats.sort_values('mean_max_aqi', ascending=False).head(top_n)

section_divider(st)

# =============================================================================
# CHART - EXACT LOGIC FROM NOTEBOOK
# =============================================================================
section_label(st, f"Top {top_n} Counties by Acute Pollution")

fig = px.bar(
    acute_top.sort_values('mean_max_aqi_display', ascending=False),
    x='mean_max_aqi_display',
    y='County',
    color='State',
    orientation='h',
    hover_data={
        'State': True,
        'mean_median_aqi': ':.1f',
        'mean_max_aqi': ':.1f',
        'mean_max_aqi_display': False
    },
    labels={
        'mean_max_aqi_display': 'Average Max AQI (Extreme Events)',
        'County': '',
        'State': 'State'
    },
    color_discrete_sequence=px.colors.sequential.Magma
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
    xaxis_title="Average Max AQI (Extreme Events)",
    yaxis_title=""
)

# Add danger threshold line
fig.add_vline(x=150, line_dash="dash", line_color="#c53030", 
              annotation_text="Unhealthy (150)", annotation_position="top")
fig.add_vline(x=300, line_dash="dash", line_color="#742a2a", 
              annotation_text="Hazardous (300)", annotation_position="top")

fig.update_xaxes(gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0')
fig.update_yaxes(gridcolor='#e2e8f0')

st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# INTERPRETATION
# =============================================================================
if len(acute_top) > 0:
    worst_county = acute_top.iloc[0]
    st.markdown(f"""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #ea580c; border-bottom: 1px solid #fff7ed; padding-bottom: 12px;">💡 What This Means</h4>
    <p><strong>{worst_county['County']}, {worst_county['State']}</strong> has the highest acute pollution 
    burden with an average Max AQI of <strong>{worst_county['mean_max_aqi']:.1f}</strong> over 2021-2024.</p>
    <p>Counties with high Max AQI experience <em>dangerous pollution episodes</em>—days when air quality 
    becomes immediately hazardous. These spikes often trigger health emergencies, especially for 
    vulnerable populations like children, elderly, and those with respiratory conditions.</p>
    <p style="margin-bottom: 0;"><strong>Note:</strong> Values above 300 are "Hazardous"—everyone may experience serious health effects.</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# OUTLIER EXPLANATION
# =============================================================================
if outlier_handling != "None":
    st.markdown("""
    <div class="callout-box-orange">
    <strong>⚠️ About Outliers:</strong> Some counties (especially in California and the Pacific Northwest) 
    have extreme Max AQI values exceeding 500+ due to wildfire smoke. While these values are real and 
    impactful, they can make it harder to see variation among other counties. The outlier handling 
    options help visualize the distribution while preserving the true values in the data table.
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# DATA TABLE
# =============================================================================
with st.expander("📋 View Data Table (True Values)"):
    display_df = acute_top[['County', 'State', 'mean_median_aqi', 'mean_max_aqi']].copy()
    display_df.columns = ['County', 'State', 'Mean Median AQI', 'Mean Max AQI']
    display_df = display_df.round(1)
    display_df.index = range(1, len(display_df) + 1)
    st.dataframe(display_df, use_container_width=True)
