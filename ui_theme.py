import streamlit as st


def inject_global_theme() -> None:
    """Apply a colorful dark agricultural theme and readable sidebar colors."""
    st.markdown(
        """
        <style>
            :root {
                --farm-primary: #66BB6A;
                --farm-primary-dark: #A5D6A7;
                --farm-accent: #FFCA28;
                --farm-bg: #07140B;
                --farm-surface: #102619;
                --farm-sidebar: #0B1D11;
                --farm-border: rgba(129, 199, 132, 0.28);
                --farm-text: #F4F8F1;
                --farm-muted: #B8C7B4;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(102, 187, 106, 0.22), transparent 34%),
                    radial-gradient(circle at top right, rgba(255, 202, 40, 0.14), transparent 28%),
                    linear-gradient(180deg, #07140B 0%, #0E2114 48%, #07140B 100%);
                color: var(--farm-text) !important;
            }

            [data-testid="stSidebarNav"] {
                display: none !important;
            }

            section[data-testid="stSidebar"] {
                background: var(--farm-sidebar) !important;
                border-right: 1px solid var(--farm-border);
            }

            section[data-testid="stSidebar"],
            section[data-testid="stSidebar"] *,
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] p,
            section[data-testid="stSidebar"] span,
            section[data-testid="stSidebar"] h1,
            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] h3,
            section[data-testid="stSidebar"] div,
            section[data-testid="stSidebar"] a,
            section[data-testid="stSidebar"] button {
                color: var(--farm-text) !important;
                opacity: 1 !important;
            }

            section[data-testid="stSidebar"] .stCaptionContainer,
            section[data-testid="stSidebar"] small {
                color: var(--farm-muted) !important;
            }

            section[data-testid="stSidebar"] .stPageLink a,
            section[data-testid="stSidebar"] .stPageLink a *,
            section[data-testid="stSidebar"] a[href],
            section[data-testid="stSidebar"] a[href] * {
                color: var(--farm-text) !important;
                fill: var(--farm-text) !important;
                font-weight: 700 !important;
                text-decoration: none !important;
            }

            section[data-testid="stSidebar"] .stPageLink a {
                border-radius: 10px;
                padding: 8px 10px;
            }

            section[data-testid="stSidebar"] .stPageLink a:hover,
            section[data-testid="stSidebar"] .stPageLink a[aria-current="page"] {
                background: rgba(102, 187, 106, 0.18) !important;
                color: #FFFFFF !important;
            }

            section[data-testid="stSidebar"] [data-baseweb="select"] > div,
            section[data-testid="stSidebar"] [data-baseweb="select"] > div *,
            section[data-testid="stSidebar"] input,
            section[data-testid="stSidebar"] textarea {
                background: #132A1B !important;
                border-color: rgba(129, 199, 132, 0.42) !important;
                color: var(--farm-text) !important;
            }

            section[data-testid="stSidebar"] svg {
                color: var(--farm-primary-dark) !important;
                fill: var(--farm-primary-dark) !important;
            }

            h1, h2, h3 {
                color: var(--farm-primary-dark);
                letter-spacing: 0;
            }

            div[data-testid="stMetric"],
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: var(--farm-surface);
                border: 1px solid var(--farm-border);
                border-radius: 16px;
                box-shadow: 0 18px 42px rgba(0, 0, 0, 0.28);
            }

            div[data-testid="stMetric"] {
                padding: 16px;
            }

            .stButton > button,
            [data-testid="stBaseButton-primary"],
            [data-testid="stBaseButton-secondary"] {
                border-radius: 999px;
                border: 1px solid var(--farm-primary);
                box-shadow: 0 6px 18px rgba(102, 187, 106, 0.22);
                font-weight: 700;
                transition: all 160ms ease;
            }

            .stButton > button:hover,
            [data-testid="stBaseButton-primary"]:hover,
            [data-testid="stBaseButton-secondary"]:hover {
                border-color: var(--farm-primary-dark);
                box-shadow: 0 10px 24px rgba(102, 187, 106, 0.30);
                transform: translateY(-1px);
            }

            [data-testid="stBaseButton-primary"] {
                background: var(--farm-primary);
                color: #FFFFFF !important;
            }

            [data-testid="stBaseButton-primary"] * {
                color: #FFFFFF !important;
            }

            .cart-badge {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                padding: 12px 14px;
                margin: 6px 0 12px;
                background: #132A1B;
                border: 1px solid rgba(129, 199, 132, 0.34);
                border-radius: 999px;
                box-shadow: 0 8px 22px rgba(0, 0, 0, 0.28);
                color: #FFFFFF !important;
                font-weight: 700;
            }

            .cart-badge-count {
                min-width: 32px;
                padding: 4px 10px;
                border-radius: 999px;
                background: var(--farm-primary);
                color: #FFFFFF !important;
                text-align: center;
            }

            .farm-hero-image {
                min-height: 220px;
                margin: 0 0 22px;
                border: 1px solid var(--farm-border);
                border-radius: 22px;
                background-position: center;
                background-size: cover;
                box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
                overflow: hidden;
            }

            .farm-hero-overlay {
                min-height: 220px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                padding: 28px;
                background: linear-gradient(90deg, rgba(4, 18, 8, 0.86), rgba(4, 18, 8, 0.35));
            }

            .farm-hero-overlay h1 {
                margin: 0;
                color: #FFFFFF !important;
            }

            .farm-hero-overlay p {
                max-width: 760px;
                margin: 8px 0 0;
                color: #E6F3E4 !important;
                font-size: 1.05rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero_image(title: str, subtitle: str, image_url: str) -> None:
    """Render a reusable colorful header image."""
    st.markdown(
        f"""
        <div class="farm-hero-image" style="background-image: url('{image_url}');">
            <div class="farm-hero-overlay">
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
