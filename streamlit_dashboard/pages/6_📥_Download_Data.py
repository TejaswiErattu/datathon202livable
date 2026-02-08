"""
Page 6: Download Data & Methodology
Export data and view methodology
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import apply_shared_styles, page_header, section_label, section_divider

st.set_page_config(page_title="Download & Methodology", page_icon="📥", layout="wide")

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
def compute_county_stats(df):
    county_stats = df.groupby(['State', 'County']).agg({
        'Median AQI': 'mean',
        'Max AQI': 'mean'
    }).reset_index()
    county_stats.columns = ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']
    return county_stats

@st.cache_data
def compute_all_exports(df, county_stats, percentile=90):
    """Compute all exportable datasets."""
    
    # Thresholds
    median_threshold = county_stats['mean_median_aqi'].quantile(percentile / 100)
    max_threshold = county_stats['mean_max_aqi'].quantile(percentile / 100)
    
    # Risk categories
    stats = county_stats.copy()
    stats['Risk_Category'] = 'Low Risk'
    stats.loc[(stats['mean_median_aqi'] >= median_threshold), 'Risk_Category'] = 'High Chronic'
    stats.loc[(stats['mean_max_aqi'] >= max_threshold), 'Risk_Category'] = 'High Acute'
    stats.loc[(stats['mean_median_aqi'] >= median_threshold) & 
              (stats['mean_max_aqi'] >= max_threshold), 'Risk_Category'] = 'Double Jeopardy'
    
    # Severity score
    stats['norm_median'] = (stats['mean_median_aqi'] - stats['mean_median_aqi'].min()) / \
                           (stats['mean_median_aqi'].max() - stats['mean_median_aqi'].min())
    stats['norm_max'] = (stats['mean_max_aqi'] - stats['mean_max_aqi'].min()) / \
                        (stats['mean_max_aqi'].max() - stats['mean_max_aqi'].min())
    stats['severity_score'] = (stats['norm_median'] + stats['norm_max']) / 2
    
    # Add ranks
    stats['Chronic_Rank'] = stats['mean_median_aqi'].rank(ascending=False).astype(int)
    stats['Acute_Rank'] = stats['mean_max_aqi'].rank(ascending=False).astype(int)
    stats['Severity_Rank'] = stats['severity_score'].rank(ascending=False).astype(int)
    
    return stats, median_threshold, max_threshold

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

county_stats = compute_county_stats(df)
full_stats, median_thresh, max_thresh = compute_all_exports(df, county_stats)

# =============================================================================
# PAGE CONTENT
# =============================================================================
page_header(st, "Download Data & Methodology", "Export Processed Data and Learn About Our Approach", "📥")

section_divider(st)

# =============================================================================
# DOWNLOAD SECTION
# =============================================================================
section_label(st, "Data Downloads")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #dc2626; border-bottom: 1px solid #fef2f2; padding-bottom: 12px;">🔴 Double Jeopardy Counties</h4>
    <p style="margin-bottom: 0;">Counties exceeding the 90th percentile for BOTH Mean Median AQI and Mean Max AQI (2021-2024).</p>
    </div>
    """, unsafe_allow_html=True)
    
    dj_counties = full_stats[full_stats['Risk_Category'] == 'Double Jeopardy'].copy()
    dj_export = dj_counties[['County', 'State', 'mean_median_aqi', 'mean_max_aqi', 
                             'Chronic_Rank', 'Acute_Rank', 'severity_score', 'Severity_Rank']]
    dj_export.columns = ['County', 'State', 'Mean_Median_AQI', 'Mean_Max_AQI', 
                         'Chronic_Rank', 'Acute_Rank', 'Severity_Score', 'Severity_Rank']
    dj_export = dj_export.sort_values('Severity_Score', ascending=False).round(3)
    
    st.download_button(
        label=f"📥 Download Double Jeopardy List ({len(dj_counties)} counties)",
        data=dj_export.to_csv(index=False),
        file_name="double_jeopardy_counties.csv",
        mime="text/csv"
    )

with col2:
    st.markdown("""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #9333ea; border-bottom: 1px solid #faf5ff; padding-bottom: 12px;">📈 Top Severity Counties</h4>
    <p style="margin-bottom: 0;">Top 50 counties ranked by combined Severity Score (normalized chronic + acute exposure).</p>
    </div>
    """, unsafe_allow_html=True)
    
    top_severity = full_stats.nlargest(50, 'severity_score').copy()
    severity_export = top_severity[['County', 'State', 'mean_median_aqi', 'mean_max_aqi',
                                    'norm_median', 'norm_max', 'severity_score', 
                                    'Risk_Category', 'Severity_Rank']]
    severity_export.columns = ['County', 'State', 'Mean_Median_AQI', 'Mean_Max_AQI',
                               'Norm_Chronic', 'Norm_Acute', 'Severity_Score',
                               'Risk_Category', 'Severity_Rank']
    severity_export = severity_export.round(3)
    
    st.download_button(
        label="📥 Download Top 50 Severity List",
        data=severity_export.to_csv(index=False),
        file_name="top_severity_counties.csv",
        mime="text/csv"
    )

# Full dataset download
section_label(st, "Full Processed Dataset")

st.markdown("""
<div class="info-card">
<h4 style="margin-top: 0; color: #2563eb; border-bottom: 1px solid #eff6ff; padding-bottom: 12px;">Complete County Statistics</h4>
<p style="margin-bottom: 0;">All counties with aggregated statistics, risk categories, and severity scores.</p>
</div>
""", unsafe_allow_html=True)

full_export = full_stats[['County', 'State', 'mean_median_aqi', 'mean_max_aqi',
                          'norm_median', 'norm_max', 'severity_score',
                          'Risk_Category', 'Chronic_Rank', 'Acute_Rank', 'Severity_Rank']]
full_export.columns = ['County', 'State', 'Mean_Median_AQI', 'Mean_Max_AQI',
                       'Norm_Chronic', 'Norm_Acute', 'Severity_Score',
                       'Risk_Category', 'Chronic_Rank', 'Acute_Rank', 'Severity_Rank']
full_export = full_export.sort_values('Severity_Score', ascending=False).round(3)

st.download_button(
    label=f"📥 Download Full Dataset ({len(full_export)} counties)",
    data=full_export.to_csv(index=False),
    file_name="all_county_statistics.csv",
    mime="text/csv"
)

# =============================================================================
# METHODOLOGY SECTION
# =============================================================================
st.markdown("---")
st.markdown("## 📐 Methodology")

st.markdown("""
<div class="info-card">
<h4 style="margin-top: 0; color: #2d3748;">Data Processing Pipeline</h4>
<ul>
    <li><strong>Data Source:</strong> EPA Air Quality Index Annual Summary files (2021-2024)</li>
    <li><strong>Geographic Unit:</strong> U.S. Counties</li>
    <li><strong>Aggregation:</strong> 4-year average of annual Median AQI and Max AQI per county</li>
    <li><strong>Threshold Calculation:</strong> 90th percentile computed dynamically from filtered dataset</li>
</ul>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #2563eb; border-bottom: 1px solid #eff6ff; padding-bottom: 12px;">Key Metrics Defined</h4>
    <ul>
        <li><strong>Mean Median AQI:</strong> Average of yearly Median AQI values (2021-2024). 
        Represents typical daily air quality—the "daily grind" of chronic exposure.</li>
        <br>
        <li><strong>Mean Max AQI:</strong> Average of yearly Max AQI values (2021-2024). 
        Represents peak pollution events—acute exposure episodes like wildfires or inversions.</li>
        <br>
        <li><strong>Severity Score:</strong> (Normalized Median + Normalized Max) / 2. 
        A single 0-1 metric combining both dimensions for overall ranking.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
    <h4 style="margin-top: 0; color: #dc2626; border-bottom: 1px solid #fef2f2; padding-bottom: 12px;">Risk Categories</h4>
    <ul>
        <li><strong style="color: #22c55e;">Low Risk:</strong> Below 90th percentile on both metrics</li>
        <br>
        <li><strong style="color: #eab308;">High Chronic:</strong> Above 90th percentile for Median AQI only</li>
        <br>
        <li><strong style="color: #f97316;">High Acute:</strong> Above 90th percentile for Max AQI only</li>
        <br>
        <li><strong style="color: #dc2626;">Double Jeopardy:</strong> Above 90th percentile for BOTH metrics</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

section_divider(st)

# =============================================================================
# LIMITATIONS
# =============================================================================
section_label(st, "Important Limitations")

st.markdown("""
<div class="callout-box-orange">
<p style="margin-top: 0;"><strong>This analysis has several limitations that users should consider:</strong></p>
<ul>
    <li><strong>Monitoring Coverage:</strong> Not all counties have continuous air quality monitoring. 
    Counties with fewer monitoring stations may have less reliable data, and some rural areas are underrepresented.</li>
    <br>
    <li><strong>Outlier Events:</strong> Extreme Max AQI values (often exceeding 500) from wildfire smoke 
    can disproportionately affect averages. We provide outlier handling options, but true values 
    reflect real exposures.</li>
    <br>
    <li><strong>Temporal Aggregation:</strong> 4-year averages smooth out year-to-year variation. 
    A county that dramatically improved in 2024 may still appear high-risk due to earlier years.</li>
    <br>
    <li><strong>Population Weighting:</strong> This analysis treats all counties equally. 
    A county with 10,000 residents counts the same as one with 10 million. 
    Population-weighted analyses may yield different priorities.</li>
    <br>
    <li><strong>Single Pollutant Focus:</strong> AQI is a composite index. Counties may face different 
    primary pollutants (PM2.5 vs. ozone) requiring different interventions.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("""
<div class="footer">
    <p style="margin: 0 0 8px 0;"><strong>Data Source:</strong> EPA Air Quality Index Annual Summary (2021-2024)</p>
    <p style="margin: 0; color: #94a3b8;"><strong>Dashboard:</strong> Datathon 2026 &nbsp;|&nbsp; Built with Streamlit + Plotly &nbsp;|&nbsp; <strong>Last Updated:</strong> February 2026</p>
</div>
""", unsafe_allow_html=True)
