# AirRisk Dashboard - Deployment Guide

## 🚀 Recommended Deployment Options

### Option 1: Streamlit Community Cloud (Recommended)
**Best for Streamlit apps - FREE and optimized**

1. Go to https://share.streamlit.io/
2. Connect your GitHub account
3. Deploy directly from your repository: `TejaswiErattu/datathon202livable`
4. Set the main file path: `streamlit_dashboard/app.py`
5. Deploy automatically!

**Advantages:**
- ✅ FREE hosting
- ✅ Optimized for Streamlit
- ✅ Auto-deploys from GitHub
- ✅ Handles Python dependencies automatically

### Option 2: Heroku (Alternative)
**Good for production apps**

1. Create a `Procfile` in root directory:
   ```
   web: streamlit run streamlit_dashboard/app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Use the existing `requirements.txt`

3. Deploy to Heroku

### Option 3: Railway (Alternative)
**Modern platform, easy deployment**

1. Connect your GitHub repository to Railway
2. Railway will auto-detect it as a Python app
3. Set the start command: `streamlit run streamlit_dashboard/app.py --server.port=$PORT --server.address=0.0.0.0`

## ⚠️ Why Vercel Doesn't Work Well

Vercel is optimized for:
- Static sites (React, Next.js, etc.)
- Serverless functions (short-lived)

Streamlit requires:
- ✅ Persistent Python process
- ✅ WebSocket connections
- ✅ Session state management

## 📋 Current Project Structure
```
datathon2026v2/
├── streamlit_dashboard/
│   ├── app.py (main dashboard)
│   ├── pages/ (analysis pages)
│   └── requirements_deploy.txt
├── requirements.txt (root level for deployment)
└── README.md
```

## 🎯 Next Steps
1. **Use Streamlit Community Cloud** (recommended)
2. Or try Railway/Heroku if you prefer
3. Remove Vercel deployment attempts - it's not the right platform for this app

Your dashboard is production-ready and professional - it just needs the right hosting platform! 🚀
