"""
AirRisk Dashboard - Main App (Overview Page)
Datathon 2026 - Professional Streamlit Dashboard
Author: Tejaswi Erattutaj
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
    page_title="AirRisk Dashboard",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS - Professional Product Theme
# =============================================================================
st.markdown("""
<style>
    /* ========== MODERN FONT & VARIABLES ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary-color: #0ea5e9;
        --primary-dark: #0284c7;
        --secondary-color: #64748b;
        --accent-color: #f97316;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --background: #ffffff;
        --surface: #f8fafc;
        --surface-elevated: #ffffff;
        --border-light: #e2e8f0;
        --border-medium: #cbd5e1;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --radius: 8px;
        --spacing-unit: 8px;
    }
    
    /* ========== GLOBAL RESET ========== */
    .stApp {
        background: var(--surface);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Reduce top padding */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px;
    }
    
    /* ========== TYPOGRAPHY SYSTEM ========== */
    h1 {
        color: var(--text-primary);
        font-weight: 700;
        font-size: 2rem !important;
        letter-spacing: -0.025em;
        margin-bottom: calc(var(--spacing-unit) * 2) !important;
        line-height: 1.2;
    }
    
    h2 {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.25rem !important;
        letter-spacing: -0.01em;
        margin-top: calc(var(--spacing-unit) * 4) !important;
        margin-bottom: calc(var(--spacing-unit) * 2) !important;
    }
    
    h3 {
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 1rem !important;
        margin-top: calc(var(--spacing-unit) * 3) !important;
        margin-bottom: calc(var(--spacing-unit) * 1) !important;
    }
    
    p, li {
        color: var(--text-secondary);
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    /* ========== CARD SYSTEM ========== */
    .pro-card {
        background: var(--surface-elevated);
        border: 1px solid var(--border-light);
        border-radius: var(--radius);
        padding: calc(var(--spacing-unit) * 3);
        box-shadow: var(--shadow-sm);
        margin-bottom: calc(var(--spacing-unit) * 3);
        transition: all 0.15s ease;
    }
    
    .pro-card:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--border-medium);
    }
    
    .pro-card-header {
        display: flex;
        align-items: center;
        gap: calc(var(--spacing-unit) * 1);
        margin-bottom: calc(var(--spacing-unit) * 2);
        padding-bottom: calc(var(--spacing-unit) * 2);
        border-bottom: 1px solid var(--border-light);
    }
    
    .pro-card-title {
        color: var(--text-primary);
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
    }
    
    .pro-card-icon {
        width: 16px;
        height: 16px;
        color: var(--primary-color);
    }
    
    /* ========== INFO BANNER (NEUTRAL STYLE) ========== */
    .info-banner {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: var(--radius);
        padding: calc(var(--spacing-unit) * 2);
        margin: calc(var(--spacing-unit) * 2) 0;
        display: flex;
        align-items: flex-start;
        gap: calc(var(--spacing-unit) * 2);
    }
    
    .info-banner-icon {
        color: var(--primary-color);
        font-size: 1.25rem;
        margin-top: 2px;
    }
    
    .info-banner-content h4 {
        color: var(--text-primary);
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0 0 calc(var(--spacing-unit) * 1) 0;
    }
    
    .info-banner-content p {
        color: var(--text-secondary);
        font-size: 0.8rem;
        margin: 0;
        line-height: 1.4;
    }
    
    /* ========== METRIC CARDS ========== */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: calc(var(--spacing-unit) * 2);
        margin: calc(var(--spacing-unit) * 3) 0;
    }
    
    .metric-card {
        background: var(--surface-elevated);
        border: 1px solid var(--border-light);
        border-radius: var(--radius);
        padding: calc(var(--spacing-unit) * 3);
        text-align: center;
        transition: all 0.15s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    .metric-label {
        color: var(--text-muted);
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: calc(var(--spacing-unit) * 1);
    }
    
    .metric-value {
        color: var(--text-primary);
        font-size: 2rem;
        font-weight: 700;
        margin: calc(var(--spacing-unit) * 1) 0;
        line-height: 1;
    }
    
    .metric-helper {
        color: var(--text-muted);
        font-size: 0.7rem;
        margin: 0;
    }
    
    /* ========== CONTROLS SECTION ========== */
    .controls-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: calc(var(--spacing-unit) * 2);
    }
    
    .section-label {
        color: var(--text-muted);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin: 0;
    }
    
    /* ========== STREAMLIT COMPONENT OVERRIDES ========== */
    div[data-testid="metric-container"] {
        background: var(--surface-elevated);
        border: 1px solid var(--border-light);
        border-radius: var(--radius);
        padding: calc(var(--spacing-unit) * 3);
        box-shadow: var(--shadow-sm);
        transition: all 0.15s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    div[data-testid="metric-container"] label {
        color: var(--text-muted);
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    /* ========== STICKY TOP BAR ========== */
    .top-bar {
        background: var(--surface-elevated);
        border-bottom: 1px solid var(--border-light);
        padding: calc(var(--spacing-unit) * 2) 0;
        margin-bottom: calc(var(--spacing-unit) * 3);
        position: sticky;
        top: 0;
        z-index: 100;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .dataset-info {
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    
    .dataset-name {
        color: var(--text-primary);
        font-weight: 600;
    }
</style>""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING - Cached for performance
# =============================================================================
@st.cache_data
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
    
    /* Sidebar navigation text styling */
    section[data-testid="stSidebar"] p {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] span {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stSlider label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stCheckbox label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stNumberInput label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stDateInput label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stTimeInput label {
        color: white !important;
    }
    
    /* Sidebar navigation links and all text */
    section[data-testid="stSidebar"] a {
        color: white !important;
        text-decoration: none !important;
    }
    
    section[data-testid="stSidebar"] a:hover {
        color: #fbbf24 !important;
        text-decoration: none !important;
    }
    
    section[data-testid="stSidebar"] a:visited {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] a:active {
        color: white !important;
    }
    
    /* Force all sidebar text to be white */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Exception for form inputs which should remain readable */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] option {
        color: black !important;
    }
    
    /* Rename 'app' to 'AirRisk' in sidebar navigation */
    section[data-testid="stSidebar"] a[href="/"]:after {
        content: "AirRisk";
        color: white !important;
        font-weight: 500;
    }
    
    section[data-testid="stSidebar"] a[href="/"] {
        font-size: 0 !important;
        color: transparent !important;
        line-height: 0;
    }
    
    section[data-testid="stSidebar"] a[href="/"]:after {
        font-size: 0.9rem !important;
        color: white !important;
        display: inline-block;
        line-height: normal;
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
    st.markdown("## AirRisk")
    st.markdown('<p style="color: #94a3b8; font-size: 0.85rem; margin-top: -8px;">Air Quality Analysis Tool</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <p style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Navigation</p>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #e2e8f0; font-size: 0.9rem; line-height: 2;">
    Chronic Pollution<br>
    Extreme Spikes<br>
    Double Jeopardy<br>
    Severity Score<br>
    County Drilldown<br>
    Download Data
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

# Professional Top Bar
st.markdown("""
<div class="top-bar">
    <div class="dataset-info">
        <span class="dataset-name">EPA AQI Analysis 2021-2024</span> • 
        Last updated: February 2026 • 
        Author: Tejaswi Erattutaj
    </div>
    <div>
        <button style="background: var(--primary-color); color: white; border: none; border-radius: 6px; padding: 6px 12px; font-size: 0.8rem; cursor: pointer;">
            📄 Export Report
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# Main title - streamlined
st.markdown("""
<div style="text-align: center; margin-bottom: 24px;">
    <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 8px; color: var(--text-primary);">Air Risk Dashboard</h1>
    <p style="color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 0;">Identifying Communities Facing Chronic AND Acute Pollution Burden</p>
</div>
""", unsafe_allow_html=True)

# Project Introduction with improved formatting
st.markdown("""
<div class="pro-card">
<div class="info-banner">
<div class="info-banner-icon">ℹ️</div>
<div class="info-banner-content">
<h4>What this shows:</h4>
<p>Counties plotted by chronic vulnerability vs acute hazard scores.</p>
<h4>Why it matters:</h4>
<p>Upper-right counties face "double jeopardy" and should be prioritized for intervention.</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# INTERACTIVE CONTROLS (PROFESSIONAL CARD LAYOUT)
# =============================================================================
st.markdown("""
<div class="pro-card">
<div class="pro-card-header">
<div class="pro-card-icon">🎛️</div>
<h3 class="pro-card-title">Analysis Controls</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

with col1:
    year_range = st.slider(
        f"📅 Year Range: {2021}-{2024}", 
        min_value=2021, max_value=2024, value=(2021, 2024), step=1,
        help="Select which years of data to include in the analysis",
        key="overview_year_range"
    )

with col2:
    all_states = sorted(county_stats['State'].unique().tolist())
    all_states.insert(0, 'All States')
    selected_state = st.selectbox("🗺️ Filter by State", all_states, index=0, key="overview_state")

with col3:
    top_n_options = [5, 10, 15, 20, 25]
    top_n = st.selectbox("📊 Top N Counties", options=top_n_options, index=1, key="overview_top_n")

with col4:
    st.markdown("<br>", unsafe_allow_html=True)  # Spacing
    if st.button("🔄 Reset", help="Reset all filters to default"):
        st.session_state.overview_year_range = (2021, 2024)
        st.session_state.overview_state = 0
        st.session_state.overview_top_n = 1
        st.experimental_rerun()

# Close the controls card
st.markdown("</div>", unsafe_allow_html=True)

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
# KPI METRICS (PROFESSIONAL CARDS)
# =============================================================================
st.markdown("""
<div class="metric-grid">
<div class="metric-card">
<div class="metric-label">Total Counties</div>
<div class="metric-value">{:,}</div>
<div class="metric-helper">Counties analyzed</div>
</div>

<div class="metric-card">
<div class="metric-label">Time Period</div>
<div class="metric-value">{}</div>
<div class="metric-helper">Years of data</div>
</div>

<div class="metric-card">
<div class="metric-label">Double Jeopardy</div>
<div class="metric-value">{}</div>
<div class="metric-helper">{:.1f}% of total counties</div>
</div>

<div class="metric-card">
<div class="metric-label">Geographic Scope</div>
<div class="metric-value">{}</div>
<div class="metric-helper">Analysis coverage</div>
</div>
</div>
""".format(
    total_counties,
    f"{year_min}-{year_max}" if year_min != year_max else str(year_min),
    double_jeopardy_count,
    (double_jeopardy_count/total_counties*100),
    selected_state if selected_state != 'All States' else 'National'
), unsafe_allow_html=True)

# Section divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# =============================================================================
# DOUBLE JEOPARDY DEFINITION BOX
# =============================================================================
st.markdown('<h3 style="margin-top: 0;">How We Define Double Jeopardy</h3>', unsafe_allow_html=True)

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
    
    <p style="margin-bottom: 0;"><strong>Why it matters:</strong> These communities face a more severe health burden. Their residents do not have relief periods to recover from poor air quality and are prone to also face periodic dangerous spikes in pollution.</p>
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
    
    st.plotly_chart(fig_pie, width='stretch')

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
# FOOTER
# =============================================================================
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 8px 0;"><strong>Author:</strong> Tejaswi Erattutaj</p>
    <p style="margin: 0 0 8px 0;"><strong>Data Source:</strong> U.S. Environmental Protection Agency, Air Quality System (AQS)</p>
    <p style="margin: 0 0 8px 0;"><strong>Citation:</strong> EPA AQI Annual Summary Data, 2021-2024. Retrieved from: https://www.epa.gov/outdoor-air-quality-data</p>
    <p style="margin: 0; color: #94a3b8;"><strong>Built for:</strong> Datathon 2026 &nbsp;|&nbsp; <strong>Framework:</strong> Streamlit + Plotly</p>
</div>
""", unsafe_allow_html=True)
