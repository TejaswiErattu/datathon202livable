"""
Page 3: Double Jeopardy Analysis
Interactive Vulnerability Profile scatter plot with bar chart
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

st.set_page_config(page_title="Double Jeopardy", page_icon="🎯", layout="wide")

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

df = load_data()
if df.empty:
    st.error("No data found.")
    st.stop()

county_stats = compute_county_stats(df)

# =============================================================================
# PAGE CONTENT
# =============================================================================
page_header(st, "Vulnerability Profile Analysis", "Counties by Vulnerability (Chronic) vs Hazard (Acute) Scores", "🎯")

st.markdown("""
<div class="callout-box-red">
<strong>Understanding the Vulnerability Profile:</strong> This analysis maps counties by their 
<em>Vulnerability Score</em> (chronic daily pollution burden) versus <em>Hazard Score</em> (acute pollution events).
Counties in the <strong>High Vulnerability / High Hazard</strong> quadrant face double jeopardy—
they need <em>priority intervention</em> as they face the worst of both worlds.
</div>
""", unsafe_allow_html=True)

section_divider(st)

# =============================================================================
# FILTERS
# =============================================================================
section_label(st, "Controls")

col1, col2, col3 = st.columns(3)

with col1:
    percentile = st.slider(
        "Percentile Threshold", 
        min_value=80, max_value=99, value=90, step=1,
        help="Counties above this percentile for BOTH metrics qualify as Double Jeopardy"
    )

with col2:
    states = ['All States'] + sorted(county_stats['State'].unique().tolist())
    selected_state = st.selectbox("Filter by State", states, key="dj_state")

with col3:
    top_n = st.slider("Top N for Bar Chart", min_value=5, max_value=25, value=10, step=5)

# Filter data
if selected_state != 'All States':
    filtered_stats = county_stats[county_stats['State'] == selected_state].copy()
else:
    filtered_stats = county_stats.copy()

# =============================================================================
# COMPUTE NORMALIZED SCORES (Vulnerability & Hazard)
# =============================================================================
stats_with_scores = filtered_stats.copy()

# Normalize to 0-1 scale (Min-Max normalization)
min_median = stats_with_scores['mean_median_aqi'].min()
max_median = stats_with_scores['mean_median_aqi'].max()
min_max = stats_with_scores['mean_max_aqi'].min()
max_max = stats_with_scores['mean_max_aqi'].max()

# Avoid division by zero
if max_median != min_median:
    stats_with_scores['vulnerability_score'] = (stats_with_scores['mean_median_aqi'] - min_median) / (max_median - min_median)
else:
    stats_with_scores['vulnerability_score'] = 0.5

if max_max != min_max:
    stats_with_scores['hazard_score'] = (stats_with_scores['mean_max_aqi'] - min_max) / (max_max - min_max)
else:
    stats_with_scores['hazard_score'] = 0.5

# Assign risk categories based on mean lines (for coloring)
mean_vuln = stats_with_scores['vulnerability_score'].mean()
mean_hazard = stats_with_scores['hazard_score'].mean()

stats_with_scores['risk_category'] = 'Low Risk'
stats_with_scores.loc[(stats_with_scores['vulnerability_score'] >= mean_vuln) & 
                      (stats_with_scores['hazard_score'] < mean_hazard), 'risk_category'] = 'High Vulnerability'
stats_with_scores.loc[(stats_with_scores['vulnerability_score'] < mean_vuln) & 
                      (stats_with_scores['hazard_score'] >= mean_hazard), 'risk_category'] = 'High Hazard'
stats_with_scores.loc[(stats_with_scores['vulnerability_score'] >= mean_vuln) & 
                      (stats_with_scores['hazard_score'] >= mean_hazard), 'risk_category'] = 'Double Jeopardy'

# Compute combined severity score for ranking
stats_with_scores['severity_score'] = (stats_with_scores['vulnerability_score'] + stats_with_scores['hazard_score']) / 2

# Add ranks
stats_with_scores['Vulnerability_Rank'] = stats_with_scores['vulnerability_score'].rank(ascending=False).astype(int)
stats_with_scores['Hazard_Rank'] = stats_with_scores['hazard_score'].rank(ascending=False).astype(int)

# =============================================================================
# METRICS
# =============================================================================
col1, col2, col3, col4 = st.columns(4)

dj_count = len(stats_with_scores[stats_with_scores['risk_category'] == 'Double Jeopardy'])
high_vuln = len(stats_with_scores[stats_with_scores['risk_category'] == 'High Vulnerability'])
high_hazard = len(stats_with_scores[stats_with_scores['risk_category'] == 'High Hazard'])
low_risk = len(stats_with_scores[stats_with_scores['risk_category'] == 'Low Risk'])

with col1:
    st.metric("🔴 Double Jeopardy", dj_count)
with col2:
    st.metric("🟡 High Vulnerability Only", high_vuln)
with col3:
    st.metric("🟠 High Hazard Only", high_hazard)
with col4:
    st.metric("🟢 Low Risk", low_risk)

section_divider(st)

# =============================================================================
# SIDE-BY-SIDE: BAR CHART + VULNERABILITY PROFILE SCATTER
# =============================================================================
section_label(st, "Vulnerability Profile Dashboard")

col_bar, col_scatter = st.columns([1, 1.5])

# -----------------------------------------------------------------------------
# LEFT: Bar Chart (Top N by Severity Score) - SORTED DESCENDING
# -----------------------------------------------------------------------------
with col_bar:
    st.markdown("#### Top Counties by Combined Severity")
    
    # Sort by severity descending, take top N
    top_counties = stats_with_scores.sort_values('severity_score', ascending=False).head(top_n)
    
    # For horizontal bar, ascending=True puts highest at top visually
    top_counties_sorted = top_counties.sort_values('severity_score', ascending=True)
    
    # Color by risk category
    bar_colors = {
        'Low Risk': '#48bb78',
        'High Vulnerability': '#ecc94b',
        'High Hazard': '#ed8936',
        'Double Jeopardy': '#c53030'
    }
    
    fig_bar = px.bar(
        top_counties_sorted,
        x='severity_score',
        y='County',
        color='risk_category',
        color_discrete_map=bar_colors,
        orientation='h',
        hover_data={
            'State': True,
            'vulnerability_score': ':.3f',
            'hazard_score': ':.3f',
            'severity_score': ':.3f',
            'mean_median_aqi': ':.1f',
            'mean_max_aqi': ':.1f'
        },
        labels={
            'severity_score': 'Combined Severity Score',
            'County': '',
            'risk_category': 'Risk Category',
            'vulnerability_score': 'Vulnerability Score',
            'hazard_score': 'Hazard Score'
        },
        category_orders={'risk_category': ['Double Jeopardy', 'High Hazard', 'High Vulnerability', 'Low Risk']}
    )
    
    # Ensure y-axis maintains sorted order
    fig_bar.update_yaxes(categoryorder='array', categoryarray=top_counties_sorted['County'].tolist())
    
    fig_bar.update_layout(
        height=max(400, top_n * 35),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title=""
        ),
        margin=dict(l=10, r=10, t=40, b=40),
        xaxis_range=[0, 1]
    )
    
    fig_bar.update_xaxes(gridcolor='#e2e8f0', zeroline=True, zerolinecolor='#cbd5e0')
    fig_bar.update_yaxes(gridcolor='#e2e8f0')
    
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# RIGHT: Interactive Vulnerability Profile Scatter
# -----------------------------------------------------------------------------
with col_scatter:
    st.markdown("#### Vulnerability Profile (Interactive)")
    
    # Create scatter using Plotly Graph Objects for full control
    fig_scatter = go.Figure()
    
    # Define colors for risk categories (RdYlGn_r inspired)
    scatter_colors = {
        'Low Risk': '#1a9850',
        'High Vulnerability': '#d9ef8b',
        'High Hazard': '#fdae61',
        'Double Jeopardy': '#d73027'
    }
    
    # Add scatter points by risk category for proper legend ordering
    for category in ['Low Risk', 'High Vulnerability', 'High Hazard', 'Double Jeopardy']:
        category_data = stats_with_scores[stats_with_scores['risk_category'] == category]
        if len(category_data) > 0:
            fig_scatter.add_trace(go.Scatter(
                x=category_data['vulnerability_score'],
                y=category_data['hazard_score'],
                mode='markers',
                name=category,
                marker=dict(
                    size=10,
                    color=scatter_colors[category],
                    line=dict(width=1, color='white'),
                    opacity=0.8
                ),
                text=category_data['County'] + ', ' + category_data['State'],
                hovertemplate=(
                    "<b>%{text}</b><br>" +
                    "Vulnerability Score: %{x:.3f}<br>" +
                    "Hazard Score: %{y:.3f}<br>" +
                    "Risk Category: " + category + "<br>" +
                    "<extra></extra>"
                )
            ))
    
    # Calculate max score for reference lines and quadrant labels
    max_score = max(
        stats_with_scores['vulnerability_score'].max(),
        stats_with_scores['hazard_score'].max(),
        1.0
    )
    
    # Add diagonal reference line (y = x)
    fig_scatter.add_trace(go.Scatter(
        x=[0, max_score],
        y=[0, max_score],
        mode='lines',
        line=dict(dash='dash', color='gray', width=1.5),
        name='y = x',
        opacity=0.5,
        showlegend=False
    ))
    
    # Add horizontal mean reference line
    fig_scatter.add_hline(
        y=mean_hazard,
        line_dash="dot",
        line_color="gray",
        line_width=1,
        opacity=0.5,
        annotation_text=f"Mean Hazard ({mean_hazard:.2f})",
        annotation_position="top right",
        annotation_font_size=9,
        annotation_font_color="gray"
    )
    
    # Add vertical mean reference line
    fig_scatter.add_vline(
        x=mean_vuln,
        line_dash="dot",
        line_color="gray",
        line_width=1,
        opacity=0.5,
        annotation_text=f"Mean Vuln ({mean_vuln:.2f})",
        annotation_position="top right",
        annotation_font_size=9,
        annotation_font_color="gray"
    )
    
    # Add quadrant labels
    fig_scatter.add_annotation(x=max_score*0.75, y=max_score*0.85, text="High Vulnerability<br>High Hazard",
        showarrow=False, font=dict(size=10, color='#666'), opacity=0.7, align='center')
    fig_scatter.add_annotation(x=max_score*0.25, y=max_score*0.85, text="Low Vulnerability<br>High Hazard",
        showarrow=False, font=dict(size=10, color='#666'), opacity=0.7, align='center')
    fig_scatter.add_annotation(x=max_score*0.25, y=max_score*0.15, text="Low Vulnerability<br>Low Hazard",
        showarrow=False, font=dict(size=10, color='#666'), opacity=0.7, align='center')
    fig_scatter.add_annotation(x=max_score*0.75, y=max_score*0.15, text="High Vulnerability<br>Low Hazard",
        showarrow=False, font=dict(size=10, color='#666'), opacity=0.7, align='center')
    
    fig_scatter.update_layout(
        title=dict(text="Vulnerability Profile", font=dict(size=14, color='#1e293b'), x=0.5),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='white',
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(
            title="Risk Category",
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#e2e8f0',
            borderwidth=1
        ),
        xaxis=dict(
            title="Vulnerability Score",
            range=[-0.05, max_score + 0.1],
            gridcolor='#e2e8f0',
            zeroline=True,
            zerolinecolor='#cbd5e0'
        ),
        yaxis=dict(
            title="Hazard Score",
            range=[-0.05, max_score + 0.1],
            gridcolor='#e2e8f0',
            zeroline=True,
            zerolinecolor='#cbd5e0'
        ),
        margin=dict(l=60, r=120, t=60, b=60)
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False
    })

# =============================================================================
# INTERPRETATION
# =============================================================================
st.markdown(f"""
<div class="info-card">
<h4 style="margin-top: 0; color: #dc2626; border-bottom: 1px solid #fef2f2; padding-bottom: 12px;">💡 How to Read This Dashboard</h4>
<p><strong>Vulnerability Score</strong> (X-axis): Normalized chronic pollution burden (0 = best, 1 = worst based on Mean Median AQI)</p>
<p><strong>Hazard Score</strong> (Y-axis): Normalized acute pollution events (0 = best, 1 = worst based on Mean Max AQI)</p>
<p><strong>Key Elements:</strong></p>
<ul>
    <li><strong>Diagonal line (y=x):</strong> Counties above this line have higher hazard than vulnerability; below means the opposite</li>
    <li><strong>Mean reference lines:</strong> Divide the chart into four quadrants based on average scores</li>
    <li><strong>Upper-right quadrant (Red):</strong> <em>Double Jeopardy</em> counties with both high vulnerability AND high hazard</li>
</ul>
<p style="margin-bottom: 0;"><strong>{dj_count} counties</strong> fall into the Double Jeopardy zone. 
These communities face both chronic daily pollution AND dangerous spikes—a compounding health crisis requiring priority intervention.</p>
</div>
""", unsafe_allow_html=True)

section_divider(st)

# =============================================================================
# DOUBLE JEOPARDY TABLE
# =============================================================================
section_label(st, "Double Jeopardy Counties")

dj_counties = stats_with_scores[stats_with_scores['risk_category'] == 'Double Jeopardy']

if len(dj_counties) > 0:
    display_df = dj_counties[['County', 'State', 'vulnerability_score', 'hazard_score', 
                              'severity_score', 'mean_median_aqi', 'mean_max_aqi']].copy()
    display_df.columns = ['County', 'State', 'Vulnerability Score', 'Hazard Score', 
                          'Severity Score', 'Mean Median AQI', 'Mean Max AQI']
    # Sort descending by severity
    display_df = display_df.sort_values('Severity Score', ascending=False).round(3)
    display_df.index = range(1, len(display_df) + 1)
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("No Double Jeopardy counties found with the current filters. Try selecting 'All States' or adjusting the threshold.")
