"""
Flask Web Application for AQI Data Analysis
Displays the EXACT graphs from the Colab notebooks using matplotlib/seaborn.
"""

from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import base64
import os
import re

print("Creating Flask app...")
app = Flask(__name__)
print(f"Flask app created: {app}")

# Get the parent directory where CSV files are located
DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_data():
    """Load and combine all AQI datasets - EXACT as in notebook."""
    file_paths = [
        os.path.join(DATA_DIR, "annual_aqi_by_county_2021.csv"),
        os.path.join(DATA_DIR, "annual_aqi_by_county_2022.csv"),
        os.path.join(DATA_DIR, "annual_aqi_by_county_2023.csv"),
        os.path.join(DATA_DIR, "annual_aqi_by_county_2024.csv"),
        os.path.join(DATA_DIR, "Access_to_a_Livable_Planet_Dataset.csv")
    ]
    
    df_list = []
    for file in file_paths:
        if os.path.exists(file):
            current_df = pd.read_csv(file)
            match = re.search(r'(\d{4})\.csv', file)
            if match:
                year = int(match.group(1))
                current_df['Year'] = year
            else:
                current_df['Year'] = None
            df_list.append(current_df)
    
    df = pd.concat(df_list, ignore_index=True)
    return df


def get_region_map():
    """Return state to region mapping - EXACT as in notebook."""
    return {
        'Alabama': 'South', 'Alaska': 'West', 'Arizona': 'West', 'Arkansas': 'South',
        'California': 'West', 'Colorado': 'West', 'Connecticut': 'Northeast',
        'Delaware': 'South', 'District Of Columbia': 'South', 'Florida': 'South',
        'Georgia': 'South', 'Hawaii': 'West', 'Idaho': 'West', 'Illinois': 'Midwest',
        'Indiana': 'Midwest', 'Iowa': 'Midwest', 'Kansas': 'Midwest', 'Kentucky': 'South',
        'Louisiana': 'South', 'Maine': 'Northeast', 'Maryland': 'South', 'Massachusetts': 'Northeast',
        'Michigan': 'Midwest', 'Minnesota': 'Midwest', 'Mississippi': 'South', 'Missouri': 'Midwest',
        'Montana': 'West', 'Nebraska': 'Midwest', 'Nevada': 'West', 'New Hampshire': 'Northeast',
        'New Jersey': 'Northeast', 'New Mexico': 'West', 'New York': 'Northeast',
        'North Carolina': 'South', 'North Dakota': 'Midwest', 'Ohio': 'Midwest',
        'Oklahoma': 'South', 'Oregon': 'West', 'Pennsylvania': 'Northeast', 'Rhode Island': 'Northeast',
        'South Carolina': 'South', 'South Dakota': 'Midwest', 'Tennessee': 'South',
        'Texas': 'South', 'Utah': 'West', 'Vermont': 'Northeast', 'Virginia': 'South',
        'Washington': 'West', 'West Virginia': 'South', 'Wisconsin': 'Midwest', 'Wyoming': 'West'
    }


def fig_to_base64():
    """Convert current matplotlib figure to base64 string."""
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()
    return img_base64


# Load data once at startup
df = load_data()
df['Region'] = df['State'].map(get_region_map())

# Pre-calculate grouped data - EXACT as in notebook
unhealthy_columns = ['Unhealthy Days', 'Very Unhealthy Days', 'Hazardous Days']
df_grouped_state = df.groupby('State')[unhealthy_columns].sum().reset_index()
df_grouped_county = df.groupby(['State', 'County'])[unhealthy_columns].sum().reset_index()


def create_graph1_top_states():
    """EXACT: Top 10 States by Total Unhealthy Days bar plot from notebook"""
    df_grouped = df_grouped_state.copy()
    df_grouped['Total Unhealthy Days'] = df_grouped[unhealthy_columns].sum(axis=1)
    df_grouped = df_grouped.sort_values(by='Total Unhealthy Days', ascending=False).reset_index(drop=True)
    top_10_states = df_grouped.head(10)
    
    # EXACT code from notebook
    plt.figure(figsize=(12, 7))
    sns.barplot(x='State', y='Total Unhealthy Days', data=top_10_states, palette='viridis', hue='State', legend=False)
    plt.xlabel('State')
    plt.ylabel('Total Unhealthy, Very Unhealthy, and Hazardous Days')
    plt.title('Top 10 States by Total Unhealthy, Very Unhealthy, and Hazardous Days (2021-2024)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig_to_base64()


def create_graph2_state_trends():
    """EXACT: Annual Trends for Top States line plot from notebook"""
    df_grouped = df_grouped_state.copy()
    df_grouped['Total Unhealthy Days'] = df_grouped[unhealthy_columns].sum(axis=1)
    top_10_states = df_grouped.sort_values(by='Total Unhealthy Days', ascending=False).head(10)
    
    df_state_yearly = df.groupby(['Year', 'State'])[unhealthy_columns].sum().reset_index()
    df_state_yearly['Total Unhealthy Days'] = df_state_yearly[unhealthy_columns].sum(axis=1)
    df_top_states_yearly = df_state_yearly[df_state_yearly['State'].isin(top_10_states['State'])]
    
    # EXACT code from notebook
    plt.figure(figsize=(14, 8))
    sns.lineplot(x='Year', y='Total Unhealthy Days', hue='State', data=df_top_states_yearly, marker='o')
    plt.xlabel('Year')
    plt.ylabel('Total Unhealthy, Very Unhealthy, and Hazardous Days')
    plt.title('Annual Trends of Unhealthy, Very Unhealthy, and Hazardous Days for Top States (2021-2025)')
    plt.xticks(df_top_states_yearly['Year'].unique())
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    return fig_to_base64()


def create_graph3_top_counties():
    """EXACT: Top 10 Counties by Total Unhealthy Days bar plot from notebook"""
    df_grouped = df_grouped_county.copy()
    df_grouped['Total Unhealthy Days'] = df_grouped[unhealthy_columns].sum(axis=1)
    df_grouped = df_grouped.sort_values(by='Total Unhealthy Days', ascending=False).reset_index(drop=True)
    top_10_counties = df_grouped.head(10)
    
    # EXACT code from notebook
    plt.figure(figsize=(14, 7))
    sns.barplot(x='County', y='Total Unhealthy Days', data=top_10_counties, palette='viridis', hue='County', legend=False)
    plt.xlabel('County')
    plt.ylabel('Total Unhealthy, Very Unhealthy, and Hazardous Days')
    plt.title('Top 10 Counties by Total Unhealthy, Very Unhealthy, and Hazardous Days (2021-2024)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig_to_base64()


def create_graph4_county_trends():
    """EXACT: Annual Trends for Top Counties line plot from notebook"""
    df_grouped = df_grouped_county.copy()
    df_grouped['Total Unhealthy Days'] = df_grouped[unhealthy_columns].sum(axis=1)
    top_10_counties = df_grouped.sort_values(by='Total Unhealthy Days', ascending=False).head(10)
    top_10_county_names = top_10_counties['County'].unique()
    
    df_county_yearly = df.groupby(['Year', 'State', 'County'])[unhealthy_columns].sum().reset_index()
    df_county_yearly['Total Unhealthy Days'] = df_county_yearly[unhealthy_columns].sum(axis=1)
    df_top_counties_yearly = df_county_yearly[df_county_yearly['County'].isin(top_10_county_names)]
    
    # EXACT code from notebook
    plt.figure(figsize=(16, 9))
    sns.lineplot(x='Year', y='Total Unhealthy Days', hue='County', data=df_top_counties_yearly, marker='o')
    plt.xlabel('Year')
    plt.ylabel('Total Unhealthy, Very Unhealthy, and Hazardous Days')
    plt.title('Annual Trends of Unhealthy, Very Unhealthy, and Hazardous Days for Top Counties (2021-2024)')
    plt.xticks(df_top_counties_yearly['Year'].unique())
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    
    return fig_to_base64()


def create_graph5_pollutant_comparison():
    """EXACT: Average Pollutant Exposure Days by Region from notebook"""
    df_2025 = df[df['Year'] == 2025].copy()
    pollutants = ['Days PM2.5', 'Days Ozone', 'Days NO2']
    
    available_pollutants = [p for p in pollutants if p in df_2025.columns]
    if not available_pollutants or 'Region' not in df_2025.columns:
        return None
    
    region_stats = df_2025.groupby('Region')[available_pollutants].mean().reset_index()
    melted_df = region_stats.melt(id_vars='Region', var_name='Pollutant', value_name='Avg Days')
    
    # EXACT code from notebook
    plt.figure(figsize=(12, 6))
    sns.barplot(data=melted_df, x='Region', y='Avg Days', hue='Pollutant', palette='magma')
    plt.title('Average Pollutant Exposure Days by Region (2025 Snapshot)', fontsize=15)
    plt.ylabel('Average Days per County')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    return fig_to_base64()


def create_graph6_livability_boxplot():
    """EXACT: Air Quality Livability by Region box plot from notebook"""
    df_2025 = df[df['Year'] == 2025].copy()
    
    if 'Days with AQI' not in df_2025.columns or 'Good Days' not in df_2025.columns:
        return None
    
    df_2025['Percent_Good_Days'] = (df_2025['Good Days'] / df_2025['Days with AQI']) * 100
    
    # EXACT code from notebook
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_2025, x='Region', y='Percent_Good_Days', palette='RdYlGn')
    plt.title('Air Quality "Livability" by Region (2025)', fontsize=15)
    plt.ylabel('% of Days with Good AQI')
    
    return fig_to_base64()


def create_graph7_max_aqi_strip():
    """EXACT: Peak Pollution Severity strip plot from notebook"""
    df_2025 = df[df['Year'] == 2025].copy()
    
    if 'Max AQI' not in df_2025.columns:
        return None
    
    # EXACT code from notebook
    plt.figure(figsize=(10, 6))
    sns.stripplot(data=df_2025, x='Region', y='Max AQI', jitter=True, alpha=0.5)
    plt.yscale('log')
    plt.title('Peak Pollution Severity (Max AQI) by Region (2025)', fontsize=15)
    plt.axhline(y=150, color='red', linestyle='--', label='Unhealthy Threshold')
    plt.legend()
    
    return fig_to_base64()


def create_graph8_top_median_aqi():
    """EXACT: Top 15 Counties by Overall Median AQI from notebook"""
    df_county_aggregated = df.groupby(['State', 'County']).agg(
        Overall_Median_AQI=('Median AQI', 'mean'),
        Unhealthy_Days_Sum=('Unhealthy Days', 'sum'),
        Very_Unhealthy_Days_Sum=('Very Unhealthy Days', 'sum'),
        Hazardous_Days_Sum=('Hazardous Days', 'sum')
    ).reset_index()
    
    df_county_aggregated['Total_Unhealthy_Days'] = df_county_aggregated[[
        'Unhealthy_Days_Sum', 'Very_Unhealthy_Days_Sum', 'Hazardous_Days_Sum'
    ]].sum(axis=1)
    
    df_county_aggregated_sorted = df_county_aggregated.sort_values(by='Overall_Median_AQI', ascending=False).reset_index(drop=True)
    top_15_counties_by_median_aqi = df_county_aggregated_sorted.head(15)
    
    # EXACT code from notebook
    plt.figure(figsize=(14, 7))
    sns.barplot(x='County', y='Overall_Median_AQI', data=top_15_counties_by_median_aqi, palette='viridis', hue='County', legend=False)
    plt.xlabel('County')
    plt.ylabel('Overall Median AQI')
    plt.title('Top 15 Counties by Overall Median AQI (2021-2025)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig_to_base64()


def create_graph9_chronic_pollution():
    """EXACT: Chronic Pollution Top 15 Counties from notebook"""
    county_stats = df.groupby(['State', 'County']).agg({
        'Median AQI': 'mean',
        'Max AQI': 'mean'
    }).reset_index()
    
    # EXACT code from notebook
    plt.figure(figsize=(10, 6))
    chronic_top15 = county_stats.sort_values('Median AQI', ascending=False).head(15)
    sns.barplot(data=chronic_top15, x='Median AQI', y='County', hue='State', palette='viridis')
    plt.title('Chronic Pollution: Top 15 Counties by 5-Year Avg Median AQI')
    plt.xlabel('Average Median AQI (Daily Grind)')
    plt.savefig('chronic_pollution_top15.png', bbox_inches='tight')
    
    return fig_to_base64()


def create_graph10_acute_pollution():
    """EXACT: Acute Pollution Top 15 Counties from notebook"""
    county_stats = df.groupby(['State', 'County']).agg({
        'Median AQI': 'mean',
        'Max AQI': 'mean'
    }).reset_index()
    
    top_15_severity = county_stats.sort_values('Max AQI', ascending=False).head(15)
    
    # EXACT code from notebook
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_15_severity, x='Max AQI', y='County', hue='State', palette='magma')
    plt.title('Acute Pollution: Top 15 Counties by 5-Year Avg Max AQI')
    plt.xlabel('Average Max AQI (Extreme Events)')
    plt.savefig('extreme_pollution_top15.png', bbox_inches='tight')
    
    return fig_to_base64()


def create_graph11_double_jeopardy_scatter():
    """EXACT: Double Jeopardy Scatter Plot from notebook (datathon_2026.py)"""
    county_stats = df.groupby(['State', 'County']).agg({
        'Median AQI': 'mean',
        'Max AQI': 'mean'
    }).reset_index()
    
    median_threshold = county_stats['Median AQI'].quantile(0.90)
    max_threshold = county_stats['Max AQI'].quantile(0.90)
    
    double_jeopardy = county_stats[
        (county_stats['Median AQI'] >= median_threshold) &
        (county_stats['Max AQI'] >= max_threshold)
    ]
    
    # EXACT code from notebook
    plt.figure(figsize=(12, 8))
    # Background: All counties
    plt.scatter(county_stats['Median AQI'], county_stats['Max AQI'], alpha=0.2, color='grey', label='All Counties')
    # Foreground: Double Jeopardy counties
    plt.scatter(double_jeopardy['Median AQI'], double_jeopardy['Max AQI'], color='red', label='Double Jeopardy Zone')
    
    # Annotate Top 10 worst in this zone
    for i, row in double_jeopardy.sort_values('Max AQI', ascending=False).head(10).iterrows():
        plt.annotate(f"{row['County']}, {row['State']}", (row['Median AQI'], row['Max AQI']),
                     fontsize=9, xytext=(5, 5), textcoords='offset points')
    
    plt.axvline(median_threshold, color='blue', linestyle='--', label='90th Percentile Median')
    plt.axhline(max_threshold, color='green', linestyle='--', label='90th Percentile Max')
    plt.title('The Double Jeopardy Zone: Chronic vs. Acute Pollution')
    plt.xlabel('Median AQI (Chronic)')
    plt.ylabel('Max AQI (Acute)')
    plt.legend()
    plt.savefig('double_jeopardy_scatter.png', bbox_inches='tight')
    
    return fig_to_base64()


def create_graph12_double_jeopardy_risk_map():
    """EXACT: Double Jeopardy Map with Risk Categories from notebook (untitled3.py)"""
    aqi_aggregated = df.groupby(['State', 'County']).agg(
        mean_max_aqi=('Max AQI', 'mean'),
        mean_median_aqi=('Median AQI', 'mean')
    ).reset_index()
    
    max_aqi_90th_percentile = aqi_aggregated['mean_max_aqi'].quantile(0.90)
    median_aqi_90th_percentile = aqi_aggregated['mean_median_aqi'].quantile(0.90)
    
    stats_5yr = aqi_aggregated.copy()
    c_thresh = median_aqi_90th_percentile
    a_thresh = max_aqi_90th_percentile
    
    # Define Risk Categories - EXACT from notebook
    stats_5yr['Risk_Category'] = 'Low Risk'
    stats_5yr.loc[(stats_5yr['mean_median_aqi'] >= c_thresh), 'Risk_Category'] = 'High Chronic'
    stats_5yr.loc[(stats_5yr['mean_max_aqi'] >= a_thresh), 'Risk_Category'] = 'High Acute'
    stats_5yr.loc[(stats_5yr['mean_median_aqi'] >= c_thresh) & (stats_5yr['mean_max_aqi'] >= a_thresh), 'Risk_Category'] = 'Double Jeopardy'
    
    # EXACT code from notebook
    plt.figure(figsize=(14, 9))
    palette = {'Low Risk': '#bdc3c7', 'High Chronic': '#f39c12', 'High Acute': '#e74c3c', 'Double Jeopardy': '#2c3e50'}
    
    sns.scatterplot(data=stats_5yr, x='mean_median_aqi', y='mean_max_aqi', hue='Risk_Category',
                    palette=palette, s=120, alpha=0.8, edgecolor='white')
    
    plt.axvline(c_thresh, color='#f39c12', linestyle='--', alpha=0.6, label='Chronic Threshold (Top 10%)')
    plt.axhline(a_thresh, color='#e74c3c', linestyle='--', alpha=0.6, label='Acute Threshold (Top 10%)')
    
    plt.yscale('log')
    plt.title('The Double Jeopardy Map (2021-2024 Trends)', fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('5-Year Average Median AQI (Daily Grind)', fontsize=12)
    plt.ylabel('5-Year Average Max AQI (Extreme Events - Log Scale)', fontsize=12)
    
    # Annotate top DJ counties
    dj_counties = stats_5yr[stats_5yr['Risk_Category'] == 'Double Jeopardy']
    for i, row in dj_counties.nlargest(8, 'mean_median_aqi').iterrows():
        plt.annotate(row['County'], (row['mean_median_aqi'], row['mean_max_aqi']),
                     textcoords="offset points", xytext=(5,5), ha='left', fontsize=9, fontweight='bold')
    
    plt.legend(title='Vulnerability Profile', bbox_to_anchor=(1.05, 1), loc='upper left')
    sns.despine()
    plt.tight_layout()
    
    return fig_to_base64()


def create_graph13_top_severity():
    """EXACT: Top 15 Most Severe Counties from notebook"""
    county_stats = df.groupby(['State', 'County']).agg({
        'Median AQI': 'mean',
        'Max AQI': 'mean'
    }).reset_index()
    
    top_15_severity = county_stats.sort_values('Max AQI', ascending=False).head(15)
    
    # EXACT code from notebook
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_15_severity, x='Max AQI', y='County', hue='State', palette='flare')
    plt.title('Top 15 Most Severe Counties (Targeted Intervention Model)')
    plt.xlabel('5-Year Average Max AQI')
    plt.ylabel('County')
    plt.savefig('top_15_severity.png', bbox_inches='tight')
    
    return fig_to_base64()


@app.route('/')
def index():
    """Main page with all graphs - EXACT from notebooks."""
    graphs = {}
    
    # Generate all graphs exactly as in notebooks
    graphs['graph1'] = create_graph1_top_states()
    graphs['graph2'] = create_graph2_state_trends()
    graphs['graph3'] = create_graph3_top_counties()
    graphs['graph4'] = create_graph4_county_trends()
    graphs['graph5'] = create_graph5_pollutant_comparison()
    graphs['graph6'] = create_graph6_livability_boxplot()
    graphs['graph7'] = create_graph7_max_aqi_strip()
    graphs['graph8'] = create_graph8_top_median_aqi()
    graphs['graph9'] = create_graph9_chronic_pollution()
    graphs['graph10'] = create_graph10_acute_pollution()
    graphs['graph11'] = create_graph11_double_jeopardy_scatter()
    graphs['graph12'] = create_graph12_double_jeopardy_risk_map()
    graphs['graph13'] = create_graph13_top_severity()
    
    return render_template('index.html', graphs=graphs)


if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=False, host='127.0.0.1', port=5000)
