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
        --border-radius: 12px;
        --border-radius-lg: 16px;
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
    }
    
    /* ========== GLOBAL RESET & BASE ========== */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        padding: var(--spacing-xl) var(--spacing-xl);
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* ========== TYPOGRAPHY ========== */
    h1 {
        color: var(--text-primary);
        font-weight: 700;
        font-size: 2.5rem !important;
        letter-spacing: -0.025em;
        margin-bottom: var(--spacing-lg) !important;
        text-align: center;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--accent-color) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.875rem !important;
        letter-spacing: -0.015em;
        margin-top: var(--spacing-xl) !important;
        margin-bottom: var(--spacing-lg) !important;
    }
    
    h3 {
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 1.25rem !important;
        margin-top: var(--spacing-lg) !important;
        margin-bottom: var(--spacing-md) !important;
    }
    
    h4 {
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 1.125rem !important;
        margin-bottom: var(--spacing-sm) !important;
    }
    
    p, li {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
        font-weight: 400;
    }
    
    /* ========== METRIC CARDS ========== */
    div[data-testid="metric-container"] {
        background: var(--surface-elevated);
        border: 1px solid var(--border-light);
        border-radius: var(--border-radius-lg);
        padding: 24px 28px;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
        border-color: var(--primary-color);
    }
    
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--accent-color) 100%);
    }
    
    div[data-testid="metric-container"] label {
        color: var(--text-muted);
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: var(--spacing-xs);
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: var(--text-primary);
        font-weight: 700;
        font-size: 2rem !important;
        line-height: 1.2;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: var(--spacing-xs);
    }
    
    /* ========== CARDS & CONTAINERS ========== */
    .info-card {
        background: var(--surface-elevated);
        border-radius: var(--border-radius-lg);
        padding: 32px 36px;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
        margin-bottom: var(--spacing-lg);
        transition: all 0.2s ease;
    }
    
    .info-card:hover {
        box-shadow: var(--shadow-md);
        border-color: var(--border-medium);
    }
    
    .info-card h4 {
        margin-top: 0 !important;
        margin-bottom: var(--spacing-lg) !important;
        padding-bottom: var(--spacing-md);
        border-bottom: 2px solid var(--border-light);
        color: var(--text-primary);
    }
    
    .callout-box {
        background: linear-gradient(135deg, #dbeafe 0%, #dcfce7 100%);
        border-left: 4px solid var(--primary-color);
        border-radius: 0 var(--border-radius-lg) var(--border-radius-lg) 0;
        padding: 28px 32px;
        margin: var(--spacing-lg) 0;
        box-shadow: var(--shadow-sm);
        position: relative;
    }
    
    .callout-box::before {
        content: '';
        position: absolute;
        top: 16px;
        right: 16px;
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    .callout-box strong {
        color: var(--primary-dark);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fed7aa 0%, #fecaca 100%);
        border-left: 4px solid var(--accent-color);
        border-radius: 0 var(--border-radius-lg) var(--border-radius-lg) 0;
        padding: 28px 32px;
        margin: var(--spacing-lg) 0;
        color: #9a3412;
        box-shadow: var(--shadow-sm);
        position: relative;
    }
    
    .warning-box::before {
        content: '';
        position: absolute;
        top: 16px;
        right: 16px;
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    /* ========== PLOTLY STYLING ========== */
    .stPlotlyChart > div {
        background: var(--surface-elevated);
        border-radius: var(--border-radius-lg);
        padding: 20px;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
    }
    
    .stPlotlyChart > div:hover {
        box-shadow: var(--shadow-md);
    }
    
    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] a {
        color: white !important;
        text-decoration: none !important;
        transition: color 0.2s ease;
    }
    
    section[data-testid="stSidebar"] a:hover {
        color: #60a5fa !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* ========== INPUT CONTROLS ========== */
    .stSelectbox > div > div {
        background: var(--surface-elevated);
        border-radius: var(--border-radius);
        border: 1px solid var(--border-light);
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-sm);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, #0369a1 100%);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    
    /* ========== CUSTOM COMPONENTS ========== */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: var(--spacing-lg);
        margin: var(--spacing-lg) 0;
    }
    
    .controls-card {
        background: var(--surface-elevated);
        border-radius: var(--border-radius-lg);
        padding: 28px 32px;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
        margin-bottom: var(--spacing-lg);
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, var(--border-light) 50%, transparent 100%);
        margin: var(--spacing-xl) 0;
        border: none;
    }
    
    .author-credits {
        background: linear-gradient(135deg, var(--surface) 0%, #f1f5f9 100%);
        border-radius: var(--border-radius-lg);
        padding: 24px 28px;
        margin: var(--spacing-xl) 0;
        border-left: 4px solid var(--secondary-color);
        font-size: 0.9rem;
    }
    
    .data-source {
        font-size: 0.85rem;
        color: var(--text-muted);
        font-style: italic;
        margin-top: var(--spacing-lg);
        padding-top: var(--spacing-md);
        border-top: 1px solid var(--border-light);
    }
    
    /* ========== RESPONSIVE DESIGN ========== */
    @media (max-width: 768px) {
        .main .block-container {
            padding: var(--spacing-lg) var(--spacing-md);
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        h2 {
            font-size: 1.5rem !important;
        }
        
        .metric-grid {
            grid-template-columns: 1fr;
            gap: var(--spacing-md);
        }
        
        .info-card, .controls-card {
            padding: 20px 24px;
        }
    }
</style>""", unsafe_allow_html=True)

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
    
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Clean the data - handle missing values and create standardized columns
    combined_df = combined_df.dropna(subset=['County', 'State'])
    
    # Create a unified State-County identifier
    combined_df['State_County'] = combined_df['State'] + ' - ' + combined_df['County']
    
    return combined_df

@st.cache_data
def compute_county_stats(_df):
    """Compute county-level statistics - cached for performance."""
    if _df.empty:
        return pd.DataFrame()
    
    county_stats = _df.groupby(['State', 'County']).agg({
        'Days with AQI': ['mean', 'std', 'count'],
        'Good Days': 'mean',
        'Moderate Days': 'mean',
        'Unhealthy for Sensitive Groups Days': 'mean',
        'Unhealthy Days': 'mean',
        'Very Unhealthy Days': 'mean',
        'Hazardous Days': 'mean',
        'Max AQI': ['mean', 'max'],
        'Median AQI': 'mean',
        'Year': ['min', 'max']
    }).round(2)
    
    # Flatten column names
    county_stats.columns = ['_'.join(col).strip() for col in county_stats.columns]
    county_stats = county_stats.reset_index()
    
    return county_stats

# =============================================================================
# MAIN APP
# =============================================================================
def main():
    """Main application function."""
    
    # Load data
    with st.spinner('Loading air quality data...'):
        df = load_data()
        county_stats = compute_county_stats(df)
    
    if df.empty:
        st.error("Unable to load data. Please check that CSV files exist in the parent directory.")
        return
    
    # Header with professional styling
    st.markdown('<div class="top-bar">', unsafe_allow_html=True)
    st.title("AirRisk Dashboard")
    st.markdown("""
    **Professional Air Quality Intelligence Platform**  
    Comprehensive analysis of EPA Air Quality Index data across US counties (2021-2024)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Metrics Overview
    st.markdown("## Key Metrics Overview")
    
    # Calculate key metrics
    total_counties = len(df.groupby(['State', 'County']))
    total_records = len(df)
    avg_aqi = df['Median AQI'].mean()
    years_covered = df['Year'].nunique()
    
    # Create metric grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Counties Analyzed", 
            value=f"{total_counties:,}",
            help="Total number of unique counties in dataset"
        )
    
    with col2:
        st.metric(
            label="Data Records", 
            value=f"{total_records:,}",
            help="Total annual county records analyzed"
        )
    
    with col3:
        st.metric(
            label="Avg. Median AQI", 
            value=f"{avg_aqi:.1f}",
            help="Average median AQI across all counties and years"
        )
    
    with col4:
        st.metric(
            label="Years Covered", 
            value=f"{years_covered}",
            help="Number of years in analysis (2021-2024)"
        )
    
    # Professional information cards
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>About This Dashboard</h4>
            <p>
                This professional dashboard provides comprehensive analysis of EPA Air Quality Index (AQI) data 
                across US counties from 2021-2024. The platform offers multiple analytical perspectives:
            </p>
            <ul>
                <li><strong>Chronic Pollution:</strong> Long-term air quality trends and patterns</li>
                <li><strong>Extreme Spikes:</strong> Analysis of hazardous air quality events</li>
                <li><strong>Double Jeopardy:</strong> Communities facing multiple environmental challenges</li>
                <li><strong>Severity Scoring:</strong> Comprehensive risk assessment methodology</li>
                <li><strong>County Drilldown:</strong> Detailed local analysis capabilities</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="callout-box">
            <strong>Data Quality</strong><br>
            All analyses use EPA's official Annual Air Quality Summary data, 
            providing reliable and standardized metrics across all jurisdictions.
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Data Preview
    st.markdown("## Data Preview")
    
    with st.expander("View Raw Data Sample", expanded=False):
        st.dataframe(
            df.head(10),
            width="stretch"
        )
    
    # Distribution Overview
    st.markdown("## Air Quality Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # AQI Distribution
        fig_hist = px.histogram(
            df, 
            x='Median AQI',
            title="Distribution of Median AQI Values",
            nbins=30,
            color_discrete_sequence=['#0ea5e9']
        )
        fig_hist.update_layout(
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family="Inter"
        )
        st.plotly_chart(fig_hist, width="stretch")
    
    with col2:
        # Good Days Distribution
        fig_good = px.histogram(
            df,
            x='Good Days',
            title="Distribution of Good Air Quality Days",
            nbins=30,
            color_discrete_sequence=['#10b981']
        )
        fig_good.update_layout(
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family="Inter"
        )
        st.plotly_chart(fig_good, width="stretch")
    
    # Temporal Trends
    st.markdown("## Temporal Trends")
    
    # Annual trends
    annual_trends = df.groupby('Year').agg({
        'Median AQI': 'mean',
        'Good Days': 'mean',
        'Unhealthy Days': 'mean',
        'Max AQI': 'mean'
    }).round(2)
    
    fig_trends = go.Figure()
    
    fig_trends.add_trace(go.Scatter(
        x=annual_trends.index,
        y=annual_trends['Median AQI'],
        mode='lines+markers',
        name='Average Median AQI',
        line=dict(color='#0ea5e9', width=3),
        marker=dict(size=8)
    ))
    
    fig_trends.update_layout(
        title="Average Air Quality Trends Over Time",
        title_x=0.5,
        xaxis_title="Year",
        yaxis_title="Average Median AQI",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_trends, width="stretch")
    
    # Navigation Guide
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>Navigation Guide</h4>
        <p>Use the sidebar to navigate through different analytical perspectives:</p>
        <ul>
            <li><strong>Chronic Pollution:</strong> Identify counties with persistent air quality issues</li>
            <li><strong>Extreme Spikes:</strong> Analyze counties with severe air quality events</li>
            <li><strong>Double Jeopardy:</strong> Find areas with both chronic and acute problems</li>
            <li><strong>Severity Score:</strong> Compare counties using comprehensive risk metrics</li>
            <li><strong>County Drilldown:</strong> Deep-dive analysis of specific locations</li>
            <li><strong>Download Data:</strong> Export processed datasets for further analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Author credits and data source
    st.markdown("""
    <div class="author-credits">
        <strong>Author:</strong> Tejaswi Erattutaj<br>
        <strong>Project:</strong> Datathon 2026 - AirRisk Professional Dashboard<br>
        <strong>Last Updated:</strong> December 2024
    </div>
    
    <div class="data-source">
        <strong>Data Source:</strong> U.S. Environmental Protection Agency (EPA)<br>
        <strong>Dataset:</strong> Annual Summary - Air Quality Index by County<br>
        <strong>Coverage:</strong> 2021-2024 Annual Data<br>
        <strong>Methodology:</strong> EPA AQI calculation standards and county-level aggregation
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
