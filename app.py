from pathlib import Path

import streamlit as st

from ui_theme import inject_global_theme, render_hero_image
from utils.helpers import render_integration_badges
from utils.translations import LANGUAGE_LABEL_BY_CODE, render_language_selector, t


st.set_page_config(
    page_title="Smart Farming Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


FEATURES = [
    {
        "title_key": "dashboard",
        "summary_key": "dashboard_intro",
        "icon": "📊",
        "page": "pages/1_dashboard.py",
    },
    {
        "title_key": "ai_assistant",
        "summary_key": "ai_assistant_intro",
        "icon": "🤖",
        "page": "pages/2_ai_assistant.py",
    },
    {
        "title_key": "weather",
        "summary_key": "weather_intro",
        "icon": "⛅",
        "page": "pages/3_weather.py",
    },
    {
        "title_key": "market_trends",
        "summary_key": "market_trends_intro",
        "icon": "📈",
        "page": "pages/4_market.py",
    },
    {
        "title_key": "marketplace",
        "summary_key": "marketplace_intro",
        "icon": "🛒",
        "page": "pages/5_marketplace.py",
    },
]

BASE_DIR = Path(__file__).parent
LOCATIONS = [
    "Pune, Maharashtra",
    "Nashik, Maharashtra",
    "Indore, Madhya Pradesh",
    "Akola, Maharashtra",
    "Custom location",
]


def initialize_global_state() -> None:
    """Safely initialize global app state shared across pages."""
    defaults = {
        "lang": "en",
        "location": "Pune, Maharashtra",
        "cart": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.lang not in LANGUAGE_LABEL_BY_CODE:
        st.session_state.lang = "en"

    if not isinstance(st.session_state.cart, list):
        st.session_state.cart = []

    if "marketplace_cart" in st.session_state:
        st.session_state.cart = st.session_state.marketplace_cart


def page_exists(page_path: str) -> bool:
    """Return whether a Streamlit page file exists in the current project."""
    return (BASE_DIR / page_path).exists()


def render_page_link(page_path: str, label: str, icon: str) -> None:
    """Render a Streamlit page link when available, otherwise show a placeholder."""
    if page_path == "app.py" or page_exists(page_path):
        st.page_link(page_path, label=label, icon=icon)
    else:
        st.caption(t("coming_soon", icon=icon, label=label))


def build_sidebar() -> None:
    """Render the shared sidebar shown on the landing page."""
    with st.sidebar:
        st.title("🌱 FarmWise")
        st.caption(t("smart_farming_platform"))

        st.divider()

        st.subheader(t("global_controls"))
        render_language_selector("language_selector_home")

        saved_location = (
            st.session_state.location
            if st.session_state.location in LOCATIONS
            else "Custom location"
        )
        location_choice = st.selectbox(
            t("farm_location"),
            LOCATIONS,
            index=LOCATIONS.index(saved_location),
            key="location_choice",
        )
        if location_choice == "Custom location":
            st.text_input(t("custom_location"), key="location")
        else:
            st.session_state.location = location_choice

        cart_count = len(st.session_state.cart)
        st.markdown(
            f"""
            <div class="cart-badge">
                <span>{t("shopping_cart")}</span>
                <span class="cart-badge-count">{cart_count}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.subheader(t("farmer_profile"))
        st.success(t("online"))
        st.write(f"**{t('user')}:** Person 1")
        st.write(f"**{t('role')}:** UI / Streamlit")
        st.write(f"**{t('farm_mode')}:** Planning")

        st.divider()

        st.subheader(t("project_links"))
        render_page_link("app.py", t("home"), "🏠")
        render_page_link("pages/1_dashboard.py", t("dashboard"), "📊")
        render_page_link("pages/2_ai_assistant.py", t("ai_assistant"), "🤖")
        render_page_link("pages/3_weather.py", t("weather"), "⛅")
        render_page_link("pages/4_market.py", t("market_trends"), "📈")
        render_page_link("pages/5_marketplace.py", t("marketplace"), "🛒")

        st.divider()

        st.info(t("sidebar_help"))

        st.divider()
        render_integration_badges()


def render_feature_card(feature: dict[str, str]) -> None:
    """Render one feature overview card."""
    title = t(feature["title_key"])
    with st.container(border=True):
        st.subheader(f"{feature['icon']} {title}")
        st.write(t(feature["summary_key"]))
        render_page_link(feature["page"], t("open_feature", feature=title), "➡️")


def render_landing_page() -> None:
    """Render the home page content."""
    render_hero_image(
        t("welcome_title"),
        t("welcome_body"),
        "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1600&q=80",
    )
    st.title(t("welcome_title"))
    st.write(t("welcome_body"))

    st.divider()

    metric_cols = st.columns(4)
    metric_cols[0].metric(t("active_fields"), "12", "+2 this month")
    metric_cols[1].metric(t("crop_health"), "86%", "+4%")
    metric_cols[2].metric(t("rain_forecast"), "68%", "Next 24 hrs")
    metric_cols[3].metric(t("market_index"), "High", "Sell window")

    st.divider()

    st.header(t("platform_overview"))
    st.caption(t("platform_overview_caption"))

    first_row = st.columns(3)
    second_row = st.columns(2)

    for column, feature in zip(first_row, FEATURES[:3]):
        with column:
            render_feature_card(feature)

    for column, feature in zip(second_row, FEATURES[3:]):
        with column:
            render_feature_card(feature)

    st.divider()

    with st.container(border=True):
        st.subheader(t("current_build_focus"))
        st.write(t("current_build_focus_body"))


initialize_global_state()
inject_global_theme()
build_sidebar()
render_landing_page()
