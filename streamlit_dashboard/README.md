# AQI Double Jeopardy Dashboard

A professional Streamlit dashboard analyzing EPA Air Quality Index data (2021-2024) to identify counties facing "Double Jeopardy" - high chronic AND acute pollution exposure.

## 🚀 Quick Start

```bash
# Navigate to the dashboard directory
cd streamlit_dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 📁 Project Structure

```
streamlit_dashboard/
├── app.py                    # Main app (Overview page)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── pages/
    ├── 1_📊_Chronic_Pollution.py
    ├── 2_⚡_Extreme_Spikes.py
    ├── 3_🎯_Double_Jeopardy.py
    ├── 4_📈_Severity_Score.py
    ├── 5_🔍_County_Drilldown.py
    └── 6_📥_Download_Data.py
```

## 📊 Features

- **Overview**: KPIs, project summary, Double Jeopardy definition
- **Chronic Pollution**: Top counties by Mean Median AQI (daily exposure)
- **Extreme Spikes**: Top counties by Mean Max AQI (peak events)
- **Double Jeopardy Analysis**: Interactive scatter plot with risk categories
- **Severity Score**: Normalized combined metric
- **County Drilldown**: Individual county profiles with yearly trends
- **Download & Methodology**: Export data and view methodology

## 🎨 Design

- Minimal, modern "climate justice" aesthetic
- Colorblind-friendly palette
- Mobile-responsive layout
- Clear data storytelling with interpretive captions

## 📈 Data Source

EPA Air Quality Index Annual Summary (2021-2024)

## 👥 Credits

Datathon 2026 Team
