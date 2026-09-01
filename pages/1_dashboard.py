from pathlib import Path

import streamlit as st

from ui_theme import inject_global_theme, render_hero_image
from utils.translations import render_language_selector, t


st.set_page_config(
    page_title="Field Insights | Smart Farming Platform",
    page_icon="📊",
    layout="wide",
)

inject_global_theme()


# Temporary mock data. Person 3 and Person 4 can replace these dictionaries
# with API/database return values without changing the UI rendering functions.
MOCK_KPI_DATA = {
    "todays_temp": {"label_key": "todays_temp", "value": "29°C", "delta": "+2°C vs yesterday"},
    "soil_moisture": {"label_key": "soil_moisture", "value": "64%", "delta": "Good range"},
    "active_crop": {"label_key": "active_crop", "value": "Tomato", "delta": "Flowering stage"},
    "market_price_index": {"label_key": "market_price_index", "value": "High", "delta": "+8% this week"},
}

MOCK_WEATHER_SUMMARY = {
    "condition": "Partly cloudy",
    "rain_chance": "68%",
    "humidity": "72%",
    "wind": "11 km/h",
    "recommendation": "Irrigate lightly in the evening if rainfall is delayed.",
}

MOCK_PRICE_SUMMARY = {
    "top_crop": "Tomato",
    "current_price": "₹2,450 / quintal",
    "trend": "Upward",
    "nearby_market": "Local mandi",
    "recommendation": "Consider holding premium-grade produce for 24-48 hours.",
}

MOCK_FARM_STATUS = {
    "farm_name": "FarmWise Demo Farm",
    "location": "Pune, Maharashtra",
    "last_updated": "Today, 11:20 AM",
}

BASE_DIR = Path(__file__).resolve().parent.parent


def get_kpi_data() -> dict[str, dict[str, str]]:
    """Return dashboard KPI data for the current farm."""
    return MOCK_KPI_DATA


def get_weather_summary() -> dict[str, str]:
    """Return weather summary data for the current farm."""
    return MOCK_WEATHER_SUMMARY


def get_price_summary() -> dict[str, str]:
    """Return market price summary data for the active crop."""
    return MOCK_PRICE_SUMMARY


def get_farm_status() -> dict[str, str]:
    """Return farm profile/status data for the dashboard header."""
    return MOCK_FARM_STATUS


def page_available(page_path: str) -> bool:
    """Return whether a target Streamlit page exists."""
    return (BASE_DIR / page_path).exists()


def render_sidebar() -> None:
    """Render dashboard navigation and user status."""
    with st.sidebar:
        st.title("🌱 FarmWise")
        st.caption(t("smart_farming_platform"))

        st.divider()
        st.subheader(t("global_controls"))
        render_language_selector("language_selector_dashboard")
        st.divider()

        st.subheader(t("user_status"))
        st.success(t("online"))
        st.write(f"**{t('role')}:** UI / Streamlit")
        st.write(f"**Page:** {t('dashboard')}")

        st.divider()

        st.page_link("app.py", label=t("home"), icon="🏠")
        st.page_link("pages/1_dashboard.py", label=t("dashboard"), icon="📊")
        render_optional_page_link("pages/2_ai_assistant.py", t("ai_assistant"), "🤖")
        render_optional_page_link("pages/3_weather.py", t("weather"), "⛅")
        render_optional_page_link("pages/4_market.py", t("market_trends"), "📈")
        render_optional_page_link("pages/5_marketplace.py", t("marketplace"), "🛒")


def render_optional_page_link(page_path: str, label: str, icon: str) -> None:
    """Render navigation when a target page exists, or a small placeholder."""
    if page_available(page_path):
        st.page_link(page_path, label=label, icon=icon)
    else:
        st.caption(t("coming_soon", icon=icon, label=label))


def render_header(farm_status: dict[str, str]) -> None:
    """Render the dashboard page header."""
    render_hero_image(
        t("farm_dashboard"),
        t("dashboard_intro"),
        "https://images.unsplash.com/photo-1495107334309-fcf20504a5ab?auto=format&fit=crop&w=1600&q=80",
    )
    st.title(t("farm_dashboard"))
    st.write(t("dashboard_intro"))

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        col1.write(f"**{t('farm')}:** {farm_status['farm_name']}")
        col2.write(f"**{t('location')}:** {farm_status['location']}")
        col3.write(f"**{t('updated')}:** {farm_status['last_updated']}")


def render_kpi_cards(kpi_data: dict[str, dict[str, str]]) -> None:
    """Render the top dashboard KPI summary cards."""
    st.subheader(t("today_at_a_glance"))

    columns = st.columns(4)
    for column, metric in zip(columns, kpi_data.values()):
        with column:
            with st.container(border=True):
                st.metric(
                    label=t(metric["label_key"]),
                    value=metric["value"],
                    delta=metric["delta"],
                )


def render_quick_actions() -> None:
    """Render primary dashboard actions."""
    with st.container(border=True):
        st.subheader(t("quick_actions"))
        st.write(t("quick_actions_body"))

        ask_ai = st.button(t("ask_ai"), type="primary", use_container_width=True)
        check_weather = st.button(t("weather_forecast"), use_container_width=True)

        if ask_ai:
            if page_available("pages/2_ai_assistant.py"):
                st.switch_page("pages/2_ai_assistant.py")
            st.info(t("ai_page_available"))

        if check_weather:
            if page_available("pages/3_weather.py"):
                st.switch_page("pages/3_weather.py")
            st.info(t("weather_available"))


def render_weather_summary(weather_summary: dict[str, str]) -> None:
    """Render weather summary placeholder card."""
    with st.container(border=True):
        st.subheader(t("weather_summary"))
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.metric(t("condition"), weather_summary["condition"])
        with col2:
            with st.container(border=True):
                st.metric(t("rain_chance"), weather_summary["rain_chance"])

        detail_cols = st.columns(2)
        detail_cols[0].write(f"**{t('humidity')}:** {weather_summary['humidity']}")
        detail_cols[1].write(f"**{t('wind')}:** {weather_summary['wind']}")
        st.info(weather_summary["recommendation"])


def render_price_summary(price_summary: dict[str, str]) -> None:
    """Render market price summary placeholder card."""
    with st.container(border=True):
        st.subheader(t("price_summary"))
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.metric(price_summary["top_crop"], price_summary["current_price"])
        with col2:
            with st.container(border=True):
                st.metric(t("trend"), price_summary["trend"])

        st.write(f"**{t('nearby_market')}:** {price_summary['nearby_market']}")
        st.success(price_summary["recommendation"])


def render_dashboard() -> None:
    """Render the complete dashboard page."""
    render_sidebar()
    render_header(get_farm_status())

    st.divider()
    render_kpi_cards(get_kpi_data())

    st.divider()
    left_column, right_column = st.columns([1, 1.35], gap="large")

    with left_column:
        render_quick_actions()

    with right_column:
        render_weather_summary(get_weather_summary())
        render_price_summary(get_price_summary())


render_dashboard()
