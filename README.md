# 🌍 AQI Double Jeopardy Dashboard
### Identifying Communities Facing Chronic AND Acute Pollution Burden
**Datathon 2026 - Environmental Justice Analysis Tool**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

## 🎯 Project Overview

This interactive dashboard analyzes EPA Air Quality Index data from 2021-2024 to identify U.S. counties experiencing **Double Jeopardy**—communities suffering from both persistently poor daily air quality AND dangerous pollution spikes. These areas require priority intervention for environmental justice.

## 🚀 Live Demo

**Dashboard URL**: [Deploy on Streamlit Cloud →](https://share.streamlit.io)

> **To deploy**: Use repository `DevanshiR2157/Datathon_2026`, branch `dev-Tejaswi`, main file `streamlit_dashboard/app.py`

## ✨ Key Features

### 📊 Interactive Dashboard
- **6-Page Multi-Dashboard System**: Overview, Chronic Pollution, Extreme Spikes, Double Jeopardy Analysis, Severity Scoring, County Drilldown
- **Year Range Filtering**: Dynamic analysis from 2021-2024 with interactive slider controls
- **Geographic Filtering**: State-level filtering with real-time data updates
- **Professional UI**: Inter typography, responsive design, colorblind-friendly visualizations

### 🎯 Double Jeopardy Analysis
- **Risk Categorization**: Identifies counties with High Chronic + High Acute pollution exposure
- **Interactive Scatter Plots**: Visual identification of at-risk communities
- **Statistical Thresholds**: 90th percentile analysis for both chronic and acute exposure
- **KPI Monitoring**: Real-time metrics showing affected populations and geographic distribution

### 📈 Advanced Visualizations
- **Plotly Interactive Charts**: Scatter plots, bar charts, pie charts with hover details
- **Matplotlib Integration**: High-fidelity statistical visualizations
- **Dynamic Thresholds**: Automatically calculated percentile-based risk thresholds
- **Responsive Design**: Mobile-friendly interface with professional styling

## 🗂️ Project Structure

```
Datathon2026/
├── streamlit_dashboard/           # 🎨 Main Dashboard Application
│   ├── app.py                    # 📱 Main overview page with controls
│   ├── styles.py                 # 🎨 Shared CSS styling system
│   ├── pages/                    # 📊 Multi-page dashboard
│   │   ├── 1_📊_Chronic_Pollution.py
│   │   ├── 2_⚡_Extreme_Spikes.py
│   │   ├── 3_🎯_Double_Jeopardy.py
│   │   ├── 4_📈_Severity_Score.py
│   │   ├── 5_🔍_County_Drilldown.py
│   │   └── 6_📥_Download_Data.py
│   ├── requirements_deploy.txt   # 🚀 Production dependencies
│   ├── Procfile                  # 🌐 Heroku deployment config
│   └── .streamlit/               # ⚙️ Streamlit configuration
├── annual_aqi_by_county_*.csv    # 📊 EPA AQI Data (2021-2024)
├── website/                      # 🌐 Previous Flask implementation
├── requirements.txt              # 📦 Development dependencies
└── README.md                     # 📖 This file
```

## 🛠️ Installation & Local Development

### Prerequisites
- Python 3.9+
- Git

### Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/DevanshiR2157/Datathon_2026.git
cd Datathon2026
git checkout dev-Tejaswi
```

2. **Create virtual environment**:
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate    # Windows
```

3. **Install dependencies**:
```bash
pip install -r streamlit_dashboard/requirements_deploy.txt
```

4. **Run the dashboard**:
```bash
cd streamlit_dashboard
streamlit run app.py
```

5. **Open in browser**: http://localhost:8501

## 📊 Data Sources

### EPA Air Quality Index Data
- **Years**: 2021, 2022, 2023, 2024
- **Coverage**: All U.S. counties with AQI monitoring
- **Metrics**: Median AQI (chronic exposure), Max AQI (acute exposure)
- **Source**: U.S. Environmental Protection Agency

### Double Jeopardy Methodology
- **High Chronic**: Counties ≥ 90th percentile for average Median AQI
- **High Acute**: Counties ≥ 90th percentile for average Max AQI  
- **Double Jeopardy**: Counties meeting BOTH criteria simultaneously

## 🚀 Deployment Options

### 1. Streamlit Community Cloud (Recommended)
- Visit [share.streamlit.io](https://share.streamlit.io)
- Repository: `DevanshiR2157/Datathon_2026`
- Branch: `dev-Tejaswi`
- Main file: `streamlit_dashboard/app.py`

### 2. Railway.app
- Connect GitHub repository
- Branch: `dev-Tejaswi`
- Root directory: `streamlit_dashboard`

### 3. Render.com
- Build command: `pip install -r requirements_deploy.txt`
- Start command: `streamlit run app.py --server.headless true --server.port $PORT`

### 4. Heroku
- Uses included `Procfile` and `setup.sh`
- Automatic deployment configuration included

## 🎨 Dashboard Pages

| Page | Description | Key Features |
|------|-------------|--------------|
| **Overview** | Main dashboard with KPIs | Year filtering, state selection, interactive controls |
| **Chronic Pollution** | Persistent pollution analysis | Long-term exposure trends, geographic distribution |
| **Extreme Spikes** | Acute pollution episodes | Peak pollution events, temporal analysis |
| **Double Jeopardy** | Combined risk analysis | Scatter plots, risk categorization, vulnerability mapping |
| **Severity Score** | Risk scoring system | Composite metrics, ranking system |
| **County Drilldown** | Detailed county analysis | Individual county profiles, trend analysis |
| **Download Data** | Data export functionality | CSV downloads, filtered datasets |

## 🔧 Technical Stack

- **Frontend**: Streamlit 1.31+
- **Visualization**: Plotly 5.15+, Matplotlib 3.7+, Seaborn 0.12+
- **Data Processing**: Pandas 2.0+, NumPy 1.24+
- **Styling**: Custom CSS with Inter typography
- **Deployment**: Multi-platform support (Streamlit Cloud, Railway, Render, Heroku)

## 📈 Key Metrics Dashboard

- **Total Counties Analyzed**: 3,000+ U.S. counties
- **Data Coverage**: 4 years (2021-2024) of EPA AQI data
- **Interactive Controls**: Year range, state filtering, top-N selection
- **Risk Categories**: Low Risk, High Chronic, High Acute, Double Jeopardy
- **Real-time Updates**: Dynamic filtering and recalculation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is developed for **Datathon 2026** - Environmental Justice Analysis.

## 🙏 Acknowledgments

- **EPA**: Air Quality Index data source
- **Streamlit**: Interactive dashboard framework
- **Plotly**: Advanced visualization capabilities
- **Environmental Justice Communities**: Inspiration for this analysis

---

## 🔗 Quick Links

- **Live Dashboard**: [Deploy Now →](https://share.streamlit.io)
- **GitHub Repository**: [DevanshiR2157/Datathon_2026](https://github.com/DevanshiR2157/Datathon_2026)
- **Development Branch**: `dev-Tejaswi`
- **EPA Data Source**: [AirData](https://www.epa.gov/outdoor-air-quality-data)

**Built with ❤️ for environmental justice and community health**
