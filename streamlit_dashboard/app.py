"""
AQI Double Jeopardy Dashboard - Main App (Overview Page)
Datathon 2026 - Professional Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import re

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="AQI Double Jeopardy Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS - Professional Climate Justice Theme (Polished)
# =============================================================================
st.markdown("""
<style>
    /* ========== GLOBAL STYLES ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ========== TYPOGRAPHY ========== */
    h1 {
        color: #0f172a;
        font-weight: 700;
        font-size: 2.25rem !important;
        letter-spacing: -0.025em;
        margin-bottom: 0.5rem !important;
        line-height: 1.2;
    }
    
    h2 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.5rem !important;
        letter-spacing: -0.01em;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: #334155;
        font-weight: 600;
        font-size: 1.125rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    h4 {
        color: #475569;
        font-weight: 600;
        font-size: 1rem !important;
    }
    
    p, li {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* ========== METRIC CARDS ========== */
    div[data-testid="metric-container"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 8px 24px rgba(0,0,0,0.04);
        transform: translateY(-1px);
    }
    
    div[data-testid="metric-container"] label {
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.75rem !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }
    
    /* ========== CARDS & CONTAINERS ========== */
    .info-card {
        background: white;
        border-radius: 16px;
        padding: 28px 32px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    
    .info-card h4 {
        margin-top: 0 !important;
        margin-bottom: 16px !important;
        padding-bottom: 12px;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .callout-box {
        background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 0 16px 16px 0;
        padding: 24px 28px;
        margin: 20px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    
    .callout-box strong {
        color: #1e40af;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff7ed 0%, #fef2f2 100%);
        border-left: 4px solid #f97316;
        border-radius: 0 16px 16px 0;
        padding: 24px 28px;
        margin: 20px 0;
    }
    
    .warning-box strong {
        color: #c2410c;
    }
    
    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    section[data-testid="stSidebar"] h2 {
        color: white !important;
        font-size: 1.25rem !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: #334155;
        margin: 1.5rem 0;
    }
    
    /* ========== FORM ELEMENTS ========== */
    .stSelectbox > div > div {
        border-radius: 10px;
        border-color: #e2e8f0;
        background: white;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .stSlider > div > div {
        color: #3b82f6;
    }
    
    /* Slider track */
    .stSlider [data-baseweb="slider"] {
        margin-top: 8px;
    }
    
    /* ========== EXPANDER ========== */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        border: 1px solid #e2e8f0;
        border-top: none;
        border-radius: 0 0 12px 12px;
        background: white;
    }
    
    /* ========== DATAFRAME ========== */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }
    
    /* ========== FOOTER ========== */
    .footer {
        text-align: center;
        padding: 32px 24px;
        color: #64748b;
        font-size: 0.85rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 64px;
        background: white;
        border-radius: 16px 16px 0 0;
    }
    
    .footer strong {
        color: #475569;
    }
    
    /* ========== SECTION DIVIDER ========== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #e2e8f0 20%, #e2e8f0 80%, transparent 100%);
        margin: 32px 0;
    }
    
    /* ========== PLOTLY CHART CONTAINER ========== */
    .stPlotlyChart {
        background: white;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING - Cached for performance
# =============================================================================
@st.cache_data
def load_data():
    """Load and combine all AQI datasets - EXACT as in original notebook."""
    # Get the parent directory where CSV files are located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.dirname(current_dir)
    
    file_paths = [
        os.path.join(data_dir, "annual_aqi_by_county_2021.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2022.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2023.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2024.csv"),
        os.path.join(data_dir, "annual_aqi_by_county_2025.csv"),
    ]
    
    df_list = []
    for file in file_paths:
        if os.path.exists(file):
            current_df = pd.read_csv(file)
            match = re.search(r'(\d{4})\.csv', file)
            if match:
                year = int(match.group(1))
                current_df['Year'] = year
            df_list.append(current_df)
    
    if not df_list:
        st.error("No data files found. Please ensure CSV files are in the parent directory.")
        return pd.DataFrame()
    
    df = pd.concat(df_list, ignore_index=True)
    return df

@st.cache_data
def compute_county_stats(_df):
    """Compute aggregated county statistics - EXACT as in original notebook."""
    county_stats = _df.groupby(['State', 'County']).agg({
        'Median AQI': 'mean',
        'Max AQI': 'mean'
    }).reset_index()
    county_stats.columns = ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']
    return county_stats

@st.cache_data
def compute_double_jeopardy(_county_stats, percentile=90):
    """Identify Double Jeopardy counties - EXACT logic from notebook."""
    median_threshold = _county_stats['mean_median_aqi'].quantile(percentile / 100)
    max_threshold = _county_stats['mean_max_aqi'].quantile(percentile / 100)
    
    stats = _county_stats.copy()
    stats['Risk_Category'] = 'Low Risk'
    stats.loc[(stats['mean_median_aqi'] >= median_threshold), 'Risk_Category'] = 'High Chronic'
    stats.loc[(stats['mean_max_aqi'] >= max_threshold), 'Risk_Category'] = 'High Acute'
    stats.loc[(stats['mean_median_aqi'] >= median_threshold) & 
              (stats['mean_max_aqi'] >= max_threshold), 'Risk_Category'] = 'Double Jeopardy'
    
    return stats, median_threshold, max_threshold

# =============================================================================
# LOAD DATA
# =============================================================================
df = load_data()

if df.empty:
    st.stop()

county_stats = compute_county_stats(df)
stats_with_risk, median_thresh, max_thresh = compute_double_jeopardy(county_stats)

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("## 🌍 AQI Dashboard")
    st.markdown('<p style="color: #94a3b8; font-size: 0.85rem; margin-top: -8px;">Air Quality Analysis Tool</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <p style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Navigation</p>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #e2e8f0; font-size: 0.9rem; line-height: 2;">
    📊 Chronic Pollution<br>
    ⚡ Extreme Spikes<br>
    🎯 Double Jeooopardy<br>
    📈 Severity Score<br>
    🔍 County Drilldown<br>
    📥 Download Data
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <p style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Data Source</p>
    <p style="color: #cbd5e1; font-size: 0.85rem;">EPA Air Quality Index<br>Annual Summary 2021-2024</p>
    """, unsafe_allow_html=True)

# =============================================================================
# MAIN CONTENT - OVERVIEW PAGE
# =============================================================================

# Header with improved styling
st.markdown("""
<div style="margin-bottom: 8px;">
    <h1 style="margin-bottom: 4px !important;">🌍 Air Quality Double Jeopardy Dashboard</h1>
    <p style="color: #64748b; font-size: 1.1rem; margin: 0;">Identifying Communities Facing Chronic AND Acute Pollution Burden</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="callout-box">
<strong>Project Summary:</strong> This dashboard analyzes EPA Air Quality Index data from 2021-2024 
to identify U.S. counties experiencing <em>Double Jeopardy</em>—communities suffering from both 
persistently poor daily air quality AND dangerous pollution spikes. These areas require 
priority intervention for environmental justice.
</div>
""", unsafe_allow_html=True)

# Section divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# =============================================================================
# INTERACTIVE CONTROLS
# =============================================================================
st.markdown('<p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;">Controls</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    year_range = st.slider(
        "Year Range to Include", 
        min_value=2021, max_value=2025, value=(2021, 2025), step=1,
        help="Select which years of data to include in the analysis",
        key="overview_year_range"
    )

with col2:
    all_states = sorted(county_stats['State'].unique().tolist())
    all_states.insert(0, 'All States')
    selected_state = st.selectbox("Filter by State", all_states, index=0, key="overview_state")

with col3:
    top_n = st.slider("Top N for Bar Chart", min_value=5, max_value=25, value=10, step=1, key="overview_top_n")

# Apply filters based on controls
year_min, year_max = year_range
df_filtered = df[(df['Year'] >= year_min) & (df['Year'] <= year_max)].copy()

# Recalculate county stats with filtered years
county_stats_filtered = df_filtered.groupby(['State', 'County']).agg({
    'Median AQI': 'mean',
    'Max AQI': 'mean'
}).reset_index()
county_stats_filtered.columns = ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']

# Filter by state if selected
if selected_state != 'All States':
    county_stats_display = county_stats_filtered[county_stats_filtered['State'] == selected_state].copy()
else:
    county_stats_display = county_stats_filtered.copy()

# Compute Double Jeopardy with filtered data
stats_with_risk, median_thresh, max_thresh = compute_double_jeopardy(county_stats_display)
double_jeopardy_count = len(stats_with_risk[stats_with_risk['Risk_Category'] == 'Double Jeopardy'])

# Section divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# =============================================================================
# KPI CARDS
# =============================================================================
st.markdown('<p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;">Key Metrics at a Glance</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

total_counties = len(county_stats_display)
top_state = stats_with_risk[stats_with_risk['Risk_Category'] == 'Double Jeopardy']['State'].value_counts()
top_state_name = top_state.index[0] if len(top_state) > 0 else "N/A"
top_state_count = top_state.iloc[0] if len(top_state) > 0 else 0

with col1:
    st.metric(
        label="Total Counties Analyzed",
        value=f"{total_counties:,}"
    )

with col2:
    years_text = f"{year_min}-{year_max}" if year_min != year_max else str(year_min)
    st.metric(
        label="Year Range",
        value=years_text,
        help="Currently analyzing data from selected year range"
    )

with col3:
    st.metric(
        label="Double Jeopardy Counties",
        value=f"{double_jeopardy_count}",
        delta=f"{(double_jeopardy_count/total_counties*100):.1f}% of total"
    )

with col4:
    if selected_state != 'All States':
        state_display = selected_state
        state_help = f"Filtered to show only {selected_state} counties"
    else:
        state_display = "All States"
        state_help = "Showing data for all states"
    
    st.metric(
        label="Geographic Filter",
        value=state_display,
        help=state_help
    )

# Section divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# =============================================================================
# DOUBLE JEOPARDY DEFINITION BOX
# =============================================================================
st.markdown('<h3 style="margin-top: 0;">🎯 How We Define Double Jeopardy</h3>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="info-card">
    <h4 style="color: #dc2626; margin-top: 0; border-bottom: 1px solid #fef2f2; padding-bottom: 12px;">Double Jeopardy = High Chronic + High Acute</h4>
    
    <p>A county qualifies as <strong>Double Jeopardy</strong> if it meets BOTH criteria:</p>
    
    <ul>
        <li><strong>High Chronic Exposure:</strong> 4-year average Median AQI ≥ 90th percentile<br>
        <span style="color: #64748b; font-size: 0.9rem;">→ Persistent daily pollution burden affecting long-term health</span></li>
        <br>
        <li><strong>High Acute Exposure:</strong> 4-year average Max AQI ≥ 90th percentile<br>
        <span style="color: #64748b; font-size: 0.9rem;">→ Dangerous pollution spikes causing immediate health risks</span></li>
    </ul>
    
    <p style="margin-bottom: 0;"><strong>Why it matters:</strong> These communities face a compounding health burden—
    their residents never get relief from poor air quality AND face periodic dangerous episodes.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Risk category breakdown pie chart
    risk_counts = stats_with_risk['Risk_Category'].value_counts()
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        hole=0.5,
        marker_colors=['#48bb78', '#ecc94b', '#ed8936', '#c53030'],
        textinfo='percent+label',
        textposition='outside'
    )])
    
    fig_pie.update_layout(
        title=dict(text="Risk Category Distribution", font_size=14),
        showlegend=False,
        margin=dict(t=60, b=20, l=20, r=20),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

# Section divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# =============================================================================
# THRESHOLDS DISPLAY
# =============================================================================
st.markdown('<p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;">Current Thresholds</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="info-card" style="text-align: center;">
        <h4 style="color: #2563eb; margin: 0; border: none; padding: 0;">Chronic Threshold</h4>
        <p style="font-size: 2.25rem; font-weight: 700; color: #0f172a; margin: 12px 0 8px 0;">{median_thresh:.1f}</p>
        <p style="color: #64748b; margin: 0; font-size: 0.85rem;">90th percentile Mean Median AQI</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="info-card" style="text-align: center;">
        <h4 style="color: #ea580c; margin: 0; border: none; padding: 0;">Acute Threshold</h4>
        <p style="font-size: 2.25rem; font-weight: 700; color: #0f172a; margin: 12px 0 8px 0;">{max_thresh:.1f}</p>
        <p style="color: #64748b; margin: 0; font-size: 0.85rem;">90th percentile Mean Max AQI</p>
    </div>
    """, unsafe_allow_html=True)

# Section divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# =============================================================================
# QUICK PREVIEW - Double Jeopardy Scatter
# =============================================================================
st.markdown('<h3 style="margin-top: 0;">🗺️ Double Jeopardy Overview</h3>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 0.9rem; margin-top: -8px; margin-bottom: 16px;">Interactive scatter plot showing all counties by chronic vs. acute pollution levels</p>', unsafe_allow_html=True)

# Color mapping
color_map = {
    'Low Risk': '#48bb78',
    'High Chronic': '#ecc94b', 
    'High Acute': '#ed8936',
    'Double Jeopardy': '#c53030'
}

fig_scatter = px.scatter(
    stats_with_risk,
    x='mean_median_aqi',
    y='mean_max_aqi',
    color='Risk_Category',
    color_discrete_map=color_map,
    hover_name='County',
    hover_data={
        'State': True,
        'mean_median_aqi': ':.1f',
        'mean_max_aqi': ':.1f',
        'Risk_Category': True
    },
    labels={
        'mean_median_aqi': 'Mean Median AQI (Chronic)',
        'mean_max_aqi': 'Mean Max AQI (Acute)',
        'Risk_Category': 'Risk Category'
    },
    category_orders={'Risk_Category': ['Low Risk', 'High Chronic', 'High Acute', 'Double Jeopardy']}
)

# Add threshold lines
fig_scatter.add_hline(y=max_thresh, line_dash="dash", line_color="#dd6b20", 
                      annotation_text="Acute Threshold", annotation_position="top right")
fig_scatter.add_vline(x=median_thresh, line_dash="dash", line_color="#3182ce",
                      annotation_text="Chronic Threshold", annotation_position="top right")

fig_scatter.update_layout(
    height=500,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='white',
    font=dict(family="Inter, sans-serif"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=80, b=40)
)

fig_scatter.update_xaxes(gridcolor='#e2e8f0', zeroline=False)
fig_scatter.update_yaxes(gridcolor='#e2e8f0', zeroline=False)

st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("""
<div class="callout-box">
<strong>💡 How to read this chart:</strong> Each dot represents a U.S. county. Counties in the 
<span style="color: #dc2626; font-weight: 600;">upper-right quadrant (red)</span> face Double Jeopardy—
they have both high daily pollution levels AND dangerous pollution spikes. Use the sidebar navigation to 
explore detailed analysis of each risk dimension.
</div>
""", unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 8px 0;"><strong>Data Source:</strong> EPA Air Quality Index Annual Summary (2021-2024)</p>
    <p style="margin: 0; color: #94a3b8;"><strong>Built for:</strong> Datathon 2026 &nbsp;|&nbsp; <strong>Framework:</strong> Streamlit + Plotly</p>
</div>
""", unsafe_allow_html=True)
