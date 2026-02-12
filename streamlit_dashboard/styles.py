"""
Shared CSS styles for the AQI Dashboard
All pages should import and apply these styles for consistency
"""

SHARED_CSS = """
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global font family */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar navigation links - WHITE color */
    .css-1d391kg .css-1544g2n a {
        color: #FFFFFF !important;
    }
    
    .css-1d391kg .css-1544g2n a:hover {
        color: #F3F4F6 !important;
    }
    
    /* Alternative selectors for different Streamlit versions */
    [data-testid="stSidebarNav"] a {
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebarNav"] a:hover {
        color: #F3F4F6 !important;
    }
    
    /* Page navigation links */
    .css-17lntkn a, .css-1544g2n a {
        color: #FFFFFF !important;
    }
    
    .css-17lntkn a:hover, .css-1544g2n a:hover {
        color: #F3F4F6 !important;
    }
    
    /* Sidebar page links styling */
    .css-1d391kg a[href*="pages"] {
        color: #FFFFFF !important;
        font-weight: 500 !important;
    }
    
    .css-1d391kg a[href*="pages"]:hover {
        color: #F3F4F6 !important;
    }
    
    /* Additional sidebar navigation selectors */
    .css-1d391kg div[data-testid="stSidebarNav"] a {
        color: #FFFFFF !important;
    }
    
    .css-1d391kg div[data-testid="stSidebarNav"] a:hover {
        color: #F3F4F6 !important;
    }
    
    /* Sidebar navigation list items */
    .css-1d391kg li a {
        color: #FFFFFF !important;
    }
    
    .css-1d391kg li a:hover {
        color: #F3F4F6 !important;
    }

    /* Main content styling */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
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
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.2s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
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
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    
    .info-card h4 {
        margin-top: 0 !important;
        margin-bottom: 16px !important;
        padding-bottom: 12px;
        border-bottom: 1px solid #f1f5f9;
    }
    
    /* Callout boxes with different colors */
    .callout-box {
        background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
        border-left: 4px solid #3b82f6;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .callout-box strong {
        color: #1e40af;
    }
    
    .callout-box-orange {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .callout-box-orange strong {
        color: #c2410c;
    }
    
    .callout-box-red {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        border-left: 4px solid #dc2626;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .callout-box-red strong {
        color: #b91c1c;
    }
    
    .callout-box-purple {
        background: linear-gradient(135deg, #faf5ff 0%, #e9d5ff 100%);
        border-left: 4px solid #8b5cf6;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .callout-box-purple strong {
        color: #7c3aed;
    }
    
    .callout-box-teal {
        background: linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%);
        border-left: 4px solid #14b8a6;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .callout-box-teal strong {
        color: #0f766e;
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
    
    .success-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid #22c55e;
        border-radius: 0 16px 16px 0;
        padding: 24px 28px;
        margin: 20px 0;
    }
    
    .success-box strong {
        color: #16a34a;
    }
    
    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
        border-right: 1px solid #334155;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] h2 {
        color: white !important;
        font-size: 1.25rem !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: #334155;
        margin: 1.5rem 0;
    }
    
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
    
    section[data-testid="stSidebar"] p {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] span {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] div {
        color: white !important;
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
    
    /* Checkbox styling */
    .stCheckbox label span {
        font-size: 0.9rem;
        color: #475569;
    }
    
    /* ========== EXPANDER ========== */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        font-weight: 500;
        color: #334155;
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
    
    /* ========== SECTION ELEMENTS ========== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, #e2e8f0 20%, #e2e8f0 80%, transparent 100%);
        margin: 2rem 0;
    }
    
    .section-label {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e293b;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* ========== PLOTLY CHART CONTAINER ========== */
    .stPlotlyChart {
        background: white;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    /* ========== PAGE HEADER ========== */
    .page-header {
        margin-bottom: 8px;
    }
    
    .page-header h1 {
        margin-bottom: 4px !important;
    }
    
    .page-subtitle {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }
    
    /* ========== FILTER SECTION ========== */
    .filter-section {
        background: white;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
    }
</style>
"""


def apply_shared_styles(st):
    """Apply shared CSS styles to the page."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)


def page_header(st, title, subtitle=None, icon=""):
    """Render a consistent page header."""
    if subtitle:
        st.markdown(f"""
        <div class="page-header">
            <h1>{icon} {title}</h1>
            <p class="page-subtitle">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"# {icon} {title}")


def section_label(st, text):
    """Render a small uppercase section label."""
    st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)


def section_divider(st):
    """Render a section divider."""
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
