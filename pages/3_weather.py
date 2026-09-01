from pathlib import Path

import pandas as pd
import streamlit as st

from ui_theme import inject_global_theme, render_hero_image
from utils.helpers import render_integration_badges
from weather.weather_api import get_weather_data
from utils.translations import render_language_selector, t


st.set_page_config(
    page_title="Weather | Smart Farming Platform",
    page_icon="⛅",
    layout="wide",
)

inject_global_theme()


# Temporary mock weather data. Person 3 can replace this function's return value
# with a real weather API response while keeping the UI functions unchanged.
MOCK_LOCATIONS = ["Pune, Maharashtra", "Nashik, Maharashtra", "Indore, Madhya Pradesh"]

MOCK_WEATHER_DATA = {
    "current": {
        "location": "Pune, Maharashtra",
        "condition": "Partly cloudy",
        "temperature_c": 29,
        "feels_like_c": 32,
        "humidity": "72%",
        "wind": "11 km/h",
        "rain_chance": "68%",
        "farm_note_key": "farm_note",
    },
    "forecast": [
        {"day": "Today", "condition": "Cloudy", "high_c": 31, "low_c": 24, "rain_chance": "68%"},
        {"day": "Wed", "condition": "Rain", "high_c": 28, "low_c": 23, "rain_chance": "82%"},
        {"day": "Thu", "condition": "Showers", "high_c": 29, "low_c": 23, "rain_chance": "74%"},
        {"day": "Fri", "condition": "Sunny", "high_c": 32, "low_c": 24, "rain_chance": "22%"},
        {"day": "Sat", "condition": "Clear", "high_c": 33, "low_c": 25, "rain_chance": "18%"},
    ],
    "hourly": pd.DataFrame(
        {
            "Hour": ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"],
            "Temperature (C)": [24, 23, 24, 27, 30, 31, 29, 26],
            "Rain Chance (%)": [40, 45, 52, 64, 68, 72, 60, 48],
        }
    ).set_index("Hour"),
}

BASE_DIR = Path(__file__).resolve().parent.parent


def get_mock_weather_data(location: str) -> dict:
    """Return weather data for the selected location."""
    weather_data = get_weather_data(location)

    if "error" in weather_data:
        return weather_data

    weather_data["current"]["location"] = location

    return weather_data


def page_available(page_path: str) -> bool:
    """Return whether a target Streamlit page exists."""
    return (BASE_DIR / page_path).exists()


def render_optional_page_link(page_path: str, label: str, icon: str) -> None:
    """Render navigation when a target page exists, or a small placeholder."""
    if page_available(page_path):
        st.page_link(page_path, label=label, icon=icon)
    else:
        st.caption(f"{icon} {label} page coming soon")


def render_sidebar() -> None:
    """Render weather page navigation."""
    with st.sidebar:
        st.title("🌱 FarmWise")
        st.caption(t("weather_intelligence"))

        st.divider()
        st.subheader(t("global_controls"))
        render_language_selector("language_selector_weather")
        st.divider()
        render_integration_badges()
        st.divider()

        st.page_link("app.py", label=t("home"), icon="🏠")
        st.page_link("pages/1_dashboard.py", label=t("dashboard"), icon="📊")
        render_optional_page_link("pages/2_ai_assistant.py", t("ai_assistant"), "🤖")
        st.page_link("pages/3_weather.py", label=t("weather"), icon="⛅")
        render_optional_page_link("pages/4_market.py", t("market_trends"), "📈")
        render_optional_page_link("pages/5_marketplace.py", t("marketplace"), "🛒")


def render_location_selector() -> str:
    """Render location inputs and return the selected location."""
    render_hero_image(
        t("weather_forecast"),
        t("weather_intro"),
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1600&q=80",
    )
    st.title(t("weather_forecast"))
    st.write(t("weather_intro"))

    selector_col, input_col = st.columns([1, 1.4], gap="large")
    selected_location = selector_col.selectbox(t("saved_farm_location"), MOCK_LOCATIONS)
    custom_location = input_col.text_input(
        t("search_another_location"),
        placeholder=t("enter_location_placeholder"),
    )

    return custom_location.strip() or selected_location


def render_current_weather(weather_data: dict) -> None:
    """Render the current weather hero card."""
    current = weather_data["current"]

    with st.container(border=True):
        st.subheader(t("current_weather", location=current.get("location", "Unknown")))
        hero_cols = st.columns([1.2, 1, 1, 1], gap="large")

        hero_cols[0].metric(
            current.get("condition", current.get("description", "Unknown")),
            f"{current.get('temperature_c', current.get('temperature', 0))}°C",
            t("feels_like", temp=current.get("feels_like_c", current.get("feels_like", 0))),
        )
        hero_cols[1].metric(t("humidity"), current.get("humidity", "N/A"))
        hero_cols[2].metric(("wind"), current.get("wind_speed", "N/A"))
        hero_cols[3].metric(("rain_chance"), "See forecast")

        st.info(t(current.get("farm_note_key", "")) or "")


def render_five_day_forecast(weather_data: dict) -> None:
    """Render a 5-day forecast card layout."""
    st.subheader(("five_day_forecast"))

    forecast_columns = st.columns(5)

    for column, day in zip(forecast_columns, weather_data.get("forecast", [])):
        with column:
            with st.container(border=True):

                st.write(f"**{day.get('datetime', 'Unknown')}**")

                st.write(day.get("description", "Unknown"))

                st.metric(
                    "Temperature",
                    f"{day.get('temperature', 'N/A')}°C"
                )

                st.caption(
                    f"Rain chance: {day.get('rain_probability', 0):.0f}%"
                )

def render_weather_chart(weather_data: dict) -> None:
    """Render the 24-hour temperature and rain trend placeholder."""
    st.subheader(t("weather_chart_title"))
    with st.container(border=True):
        forecast = weather_data.get("forecast", [])

        if forecast:
            chart_data = {
                "Temperature": [
                    item.get("temperature", 0)
                    for item in forecast
                ]
            }

            st.line_chart(chart_data)
        else:
            st.info("Weather trend data unavailable.")

    st.caption(t("weather_chart_caption"))


def render_weather_page() -> None:
    """Render the complete weather page."""
    render_sidebar()
    location = render_location_selector()
    st.session_state.location = location
    weather_data = get_mock_weather_data(location)

    st.divider()
    render_current_weather(weather_data)

    st.divider()
    render_five_day_forecast(weather_data)

    st.divider()
    render_weather_chart(weather_data)


render_weather_page()
