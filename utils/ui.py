import html

import streamlit as st


def configure_page(title: str, page_title: str | None = None, page_icon: str = "DB"):
    """Configure Streamlit wide layout and inject shared high-contrast styles."""
    st.set_page_config(
        page_title=page_title or f"DiaBites DS | {title}",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()


def inject_css():
    """Inject global dashboard CSS for dark content and bright readable sidebar."""
    st.markdown(
        """
        <style>
            /* ======================================
               CSS Variables
               ====================================== */
            :root {
                --app-bg: #030712;
                --panel: #111827;
                --panel-2: #0B1120;
                --text: #F5F5F5;
                --secondary: #D1D5DB;
                --sidebar-bg: #F3F4F6;
                --sidebar-text: #111827;
                --sidebar-desc: #374151;
                --blue: #2563EB;
                --green: #22C55E;
                --amber: #F59E0B;
                --red: #EF4444;
                --border: rgba(209, 213, 219, 0.16);
            }

            /* ======================================
               Global Background & Text
               ====================================== */
            html, body, [data-testid="stAppViewContainer"], .stApp {
                background: var(--app-bg) !important;
                color: var(--text) !important;
            }

            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2.5rem;
            }

            /* ======================================
               Sidebar Base
               ====================================== */
            [data-testid="stSidebar"] {
                background: var(--sidebar-bg) !important;
                border-right: 1px solid rgba(17, 24, 39, 0.12);
            }

            [data-testid="stSidebar"] *,
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] small {
                color: var(--sidebar-desc) !important;
            }

            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: var(--sidebar-text) !important;
            }

            /* ======================================
               Sidebar Brand Title
               ====================================== */
            .sidebar-brand {
                font-size: 1.75rem;
                font-weight: 800;
                color: #111827 !important;
                margin: 0 0 0.35rem 0;
                letter-spacing: -0.02em;
            }

            /* ======================================
               Sidebar Description Card
               ====================================== */
            [data-testid="stSidebar"] .sidebar-panel {
                background: #FFFFFF;
                border: 1px solid rgba(17, 24, 39, 0.10);
                border-radius: 14px;
                padding: 0.85rem;
                margin: 0.45rem 0 1rem 0;
                box-shadow: 0 4px 12px rgba(17, 24, 39, 0.06);
            }

            .sidebar-panel strong {
                color: #111827 !important;
                font-size: 0.95rem;
            }

            .sidebar-panel br + * {
                color: #374151 !important;
            }

            /* ======================================
               Sidebar Navigation – Active Item
               ====================================== */
            .nav-active {
                background: #2563EB;
                color: #FFFFFF !important;
                padding: 0.6rem 1rem;
                border-radius: 12px;
                font-weight: 700;
                font-size: 0.95rem;
                margin-bottom: 0.45rem;
                box-shadow: 0 2px 8px rgba(37, 99, 235, 0.22);
                letter-spacing: 0;
            }

            /* ======================================
               Sidebar Navigation – Inactive Links
               ====================================== */
            [data-testid="stSidebar"] a {
                background: #FFFFFF !important;
                color: #374151 !important;
                border: 1px solid rgba(17, 24, 39, 0.10) !important;
                border-radius: 12px !important;
                margin-bottom: 0.45rem !important;
                padding: 0.55rem 1rem !important;
                display: block !important;
                font-weight: 600 !important;
                font-size: 0.95rem !important;
                text-decoration: none !important;
                box-shadow: 0 2px 8px rgba(17, 24, 39, 0.05) !important;
                transition: background 0.2s ease !important;
            }

            [data-testid="stSidebar"] a:hover {
                background: #E5E7EB !important;
            }

            [data-testid="stSidebar"] a span,
            [data-testid="stSidebar"] a p {
                color: #374151 !important;
                font-weight: 600 !important;
            }

            /* ======================================
               Sidebar Widget Labels
               ====================================== */
            [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
                color: var(--sidebar-text) !important;
                font-weight: 700;
            }

            .stSelectbox div[data-baseweb="select"] > div,
            .stMultiSelect div[data-baseweb="select"] > div,
            .stNumberInput input,
            .stTextInput input {
                background: #FFFFFF !important;
                color: #111827 !important;
                border-color: rgba(17, 24, 39, 0.18) !important;
            }

            /* ======================================
               Main Content – Headings
               ====================================== */
            h1, h2, h3,
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3 {
                color: #FFFFFF !important;
                letter-spacing: 0;
            }

            p, li, label, span,
            [data-testid="stMarkdownContainer"] p,
            [data-testid="stWidgetLabel"] p {
                color: var(--secondary) !important;
            }

            /* ======================================
               Hero Block
               ====================================== */
            .hero {
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 1.35rem 1.5rem;
                background:
                    linear-gradient(135deg, rgba(37, 99, 235, 0.18), rgba(34, 197, 94, 0.12)),
                    var(--panel);
                margin-bottom: 1.25rem;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
            }

            .hero-title {
                color: #FFFFFF;
                font-size: 2rem;
                line-height: 1.15;
                font-weight: 800;
                margin: 0;
            }

            .hero-copy,
            .app-description,
            .page-copy,
            .secondary-text {
                color: var(--secondary) !important;
                font-size: 1rem;
                max-width: 980px;
            }

            /* ======================================
               Metric & Section Cards
               ====================================== */
            .metric-card,
            .section-panel,
            .product-card {
                border: 1px solid var(--border);
                border-radius: 16px;
                background: var(--panel);
                padding: 20px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
            }

            .metric-card {
                min-height: 118px;
            }

            .metric-label {
                color: var(--secondary) !important;
                font-size: 0.82rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0;
                margin-bottom: 0.55rem;
            }

            .metric-value {
                color: #FFFFFF !important;
                font-size: 1.7rem;
                font-weight: 800;
                line-height: 1.1;
                overflow-wrap: anywhere;
            }

            .metric-note {
                color: var(--secondary) !important;
                font-size: 0.88rem;
                margin-top: 0.4rem;
            }

            /* ======================================
               Insight Box
               ====================================== */
            .insight-box {
                border: 1px solid rgba(34, 197, 94, 0.22);
                border-radius: 16px;
                background: rgba(17, 24, 39, 0.92);
                padding: 1rem 1.15rem;
                color: #FFFFFF !important;
                font-weight: 700;
                margin: 0.6rem 0 1rem 0;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
                font-size: 0.95rem;
                line-height: 1.55;
            }

            /* ======================================
               Badges
               ====================================== */
            .badge {
                display: inline-flex;
                align-items: center;
                border-radius: 999px;
                padding: 0.28rem 0.68rem;
                font-weight: 800;
                font-size: 0.82rem;
                color: #FFFFFF !important;
            }

            .badge-green { background: #15803D; }
            .badge-amber { background: #B45309; }
            .badge-red { background: #B91C1C; }
            .badge-blue { background: #1D4ED8; }

            /* ======================================
               Section Titles
               ====================================== */
            .section-title {
                color: #FFFFFF !important;
                font-size: 1.25rem;
                font-weight: 800;
                margin: 1.2rem 0 0.5rem;
            }

            /* ======================================
               Data Frames & Alerts
               ====================================== */
            div[data-testid="stDataFrame"] {
                border-radius: 16px;
                overflow: hidden;
            }

            div[data-testid="stAlert"] p {
                color: #111827 !important;
            }

            /* ======================================
               Chart Subtitle
               ====================================== */
            .chart-subtitle {
                color: #9CA3AF !important;
                font-size: 0.88rem;
                margin: 0.1rem 0 0.35rem 0;
                font-style: italic;
            }

            /* ======================================
               Responsive
               ====================================== */
            @media (max-width: 900px) {
                .hero-title { font-size: 1.55rem; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand(active_page: str):
    """Render the shared sidebar brand and nutrition-only navigation."""
    st.sidebar.markdown(
        '<div class="sidebar-brand">🍽️ DiaBites</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="sidebar-panel">
            <strong>Nutrition Dashboard</strong><br>
            <span style="color:#374151;font-size:0.88rem;">
            Analisis risiko produk, kualitas ekstraksi, dan rekomendasi untuk 7 profil medis.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages = [
        ("📊", "Overview", "app.py"),
        ("🔍", "Nutrition Analysis", "pages/2_Nutrition_Analysis.py"),
        ("🎯", "Recommendation Simulator", "pages/3_Recommendation_Simulator.py"),
    ]

    for icon, label, path in pages:
        if label == active_page:
            st.sidebar.markdown(
                f'<div class="nav-active">{icon} {label}</div>',
                unsafe_allow_html=True,
            )
        else:
            try:
                st.sidebar.page_link(path, label=f"{icon} {label}")
            except Exception:
                st.sidebar.markdown(
                    f'<div style="background:#FFFFFF;color:#374151;padding:0.6rem 1rem;'
                    f'border-radius:12px;margin-bottom:0.45rem;font-weight:600;font-size:0.95rem;'
                    f'border:1px solid rgba(17,24,39,0.10);">{icon} {label}</div>',
                    unsafe_allow_html=True,
                )

    st.sidebar.divider()


def sidebar_dataset_notes():
    """Render the dataset source notes in the sidebar."""
    st.sidebar.caption("Sumber data")
    st.sidebar.markdown(
        """
        <div class="sidebar-panel" style="padding:0.65rem 0.85rem;">
            <span style="font-size:0.85rem;color:#374151 !important;">
            📁 nutrition_dataset.csv<br>
            📁 yolo_dataset_quality.csv
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str):
    """Render a reusable page hero block."""
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">{html.escape(title)}</div>
            <div class="hero-copy">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str):
    """Render a high-contrast section title."""
    st.markdown(f'<div class="section-title">{html.escape(title)}</div>', unsafe_allow_html=True)


def chart_subtitle(text: str):
    """Render a small subtitle below section title for chart context."""
    st.markdown(f'<div class="chart-subtitle">{html.escape(text)}</div>', unsafe_allow_html=True)


def metric_card(label: str, value, note: str = ""):
    """Render a reusable dark metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-note">{html.escape(str(note))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_box(text: str):
    """Render an automatic insight message on a dark panel."""
    st.markdown(f'<div class="insight-box">{html.escape(text)}</div>', unsafe_allow_html=True)


def status_badge(text: str, status: str = "green") -> str:
    """Return a high-contrast HTML badge for product recommendation status."""
    badge_class = {
        "green": "badge-green",
        "red": "badge-red",
        "amber": "badge-amber",
        "blue": "badge-blue",
        "Recommended": "badge-green",
        "Caution": "badge-amber",
        "Not Recommended": "badge-red",
    }.get(status, "badge-blue")
    return f'<span class="badge {badge_class}">{html.escape(str(text))}</span>'


def empty_state(message: str):
    """Render a clear empty-state message."""
    st.info(message)
