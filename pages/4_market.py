from pathlib import Path

import pandas as pd
import streamlit as st

from ui_theme import inject_global_theme, render_hero_image
from utils.helpers import fetch_market_prices, render_integration_badges
from utils.translations import render_language_selector, t

try:
    import plotly.express as px
except Exception:
    px = None


st.set_page_config(
    page_title="Market Trends | Smart Farming Platform",
    page_icon="📈",
    layout="wide",
)

inject_global_theme()


# Temporary mock market data. Person 3 can replace get_mock_market_data()
# with an API/database-backed implementation and keep the UI layer intact.
MOCK_CATEGORIES = ["All", "Vegetables", "Fruits", "Grains", "Pulses"]
MARKET_CATEGORY_LABEL_KEYS = {
    "All": "all",
    "Vegetables": "vegetables",
    "Fruits": "fruits",
    "Grains": "grains",
    "Pulses": "pulses",
}

MOCK_MARKET_PRICES = pd.DataFrame(
    [
        {"Commodity": "Tomato", "Category": "Vegetables", "Market": "Pune Mandi", "Min Price": 2100, "Max Price": 2700, "Modal Price": 2450, "Trend": "Up"},
        {"Commodity": "Onion", "Category": "Vegetables", "Market": "Nashik Mandi", "Min Price": 1600, "Max Price": 2200, "Modal Price": 1900, "Trend": "Stable"},
        {"Commodity": "Wheat", "Category": "Grains", "Market": "Indore Mandi", "Min Price": 2350, "Max Price": 2580, "Modal Price": 2460, "Trend": "Up"},
        {"Commodity": "Soybean", "Category": "Pulses", "Market": "Ujjain Mandi", "Min Price": 4100, "Max Price": 4620, "Modal Price": 4380, "Trend": "Down"},
        {"Commodity": "Banana", "Category": "Fruits", "Market": "Jalgaon Mandi", "Min Price": 1200, "Max Price": 1800, "Modal Price": 1520, "Trend": "Stable"},
        {"Commodity": "Gram", "Category": "Pulses", "Market": "Akola Mandi", "Min Price": 5400, "Max Price": 5900, "Modal Price": 5660, "Trend": "Up"},
    ]
)

MOCK_PRICE_TRENDS = pd.DataFrame(
    {
        "Date": pd.date_range("2025-09-01", periods=366, freq="D"),
        "Tomato": [1800 + (day * 5) + ((day % 14) * 18) for day in range(366)],
        "Onion": [1700 + (day % 45) * 7 + ((day % 9) * 12) for day in range(366)],
        "Wheat": [2250 + (day * 2) + ((day % 21) * 5) for day in range(366)],
        "Soybean": [4700 - (day * 1.2) + ((day % 18) * 14) for day in range(366)],
    }
).set_index("Date")

BASE_DIR = Path(__file__).resolve().parent.parent


def get_mock_market_data() -> dict[str, pd.DataFrame | list[str]]:
    """Return market price data for commodity search, charts, and tables."""
    return fetch_market_prices(st.session_state.get("location", "Pune, Maharashtra"))


def page_available(page_path: str) -> bool:
    """Return whether a target Streamlit page exists."""
    return (BASE_DIR / page_path).exists()


def render_optional_page_link(page_path: str, label: str, icon: str) -> None:
    """Render navigation when a target page exists, or a small placeholder."""
    if page_available(page_path):
        st.page_link(page_path, label=label, icon=icon)
    else:
        st.caption(t("coming_soon", icon=icon, label=label))


def render_sidebar() -> None:
    """Render market page navigation."""
    with st.sidebar:
        st.title("🌱 FarmWise")
        st.caption(t("market_intelligence"))

        st.divider()
        st.subheader(t("global_controls"))
        render_language_selector("language_selector_market")
        st.divider()
        render_integration_badges()
        st.divider()

        st.page_link("app.py", label=t("home"), icon="🏠")
        st.page_link("pages/1_dashboard.py", label=t("dashboard"), icon="📊")
        render_optional_page_link("pages/2_ai_assistant.py", t("ai_assistant"), "🤖")
        render_optional_page_link("pages/3_weather.py", t("weather"), "⛅")
        st.page_link("pages/4_market.py", label=t("market_trends"), icon="📈")
        render_optional_page_link("pages/5_marketplace.py", t("marketplace"), "🛒")


def render_filters(market_data: dict[str, pd.DataFrame | list[str]]) -> tuple[str, str]:
    """Render crop search and category filter controls."""
    render_hero_image(
        t("market_trends"),
        t("market_trends_intro"),
        "https://images.unsplash.com/photo-1523741543316-beb7fc7023d8?auto=format&fit=crop&w=1600&q=80",
    )
    st.title(t("market_trends"))
    st.write(t("market_trends_intro"))

    search_col, category_col = st.columns([1.4, 1], gap="large")
    search_query = search_col.text_input(t("commodity_search"), placeholder="Search tomato, wheat, soybean...")
    category = category_col.selectbox(
        t("category_filter"),
        market_data["categories"],
        format_func=lambda value: t(MARKET_CATEGORY_LABEL_KEYS.get(value, "category")),
    )

    return search_query.strip(), category


def filter_market_prices(prices: pd.DataFrame, search_query: str, category: str) -> pd.DataFrame:
    """Filter market prices by search query and selected category."""
    filtered_prices = prices.copy()

    if category != "All":
        filtered_prices = filtered_prices[filtered_prices["Category"] == category]

    if search_query:
        search_mask = filtered_prices["Commodity"].str.contains(search_query, case=False, na=False)
        filtered_prices = filtered_prices[search_mask]

    return filtered_prices


def render_summary_metrics(filtered_prices: pd.DataFrame) -> None:
    """Render quick market summary metrics."""
    if filtered_prices.empty:
        st.warning(t("no_commodities"))
        return

    best_price_row = filtered_prices.sort_values("Modal Price", ascending=False).iloc[0]
    rising_count = int((filtered_prices["Trend"] == "Up").sum())

    metric_cols = st.columns(3)
    with metric_cols[0]:
        with st.container(border=True):
            st.metric(t("commodities_found"), len(filtered_prices))
    with metric_cols[1]:
        with st.container(border=True):
            st.metric(t("highest_modal_price"), f"₹{best_price_row['Modal Price']:,.0f}", best_price_row["Commodity"])
    with metric_cols[2]:
        with st.container(border=True):
            st.metric(t("rising_markets"), rising_count)


def prepare_price_trend_data(trends: pd.DataFrame) -> pd.DataFrame:
    """Convert wide trend data into long-form records for Plotly hover details."""
    trend_data = trends.reset_index().melt(
        id_vars="Date",
        var_name="Crop",
        value_name="Price",
    )
    trend_data["Formatted Price"] = trend_data["Price"].map(lambda price: f"₹{price:,.0f}")
    return trend_data


def render_price_trend_chart(trends: pd.DataFrame) -> None:
    """Render interactive price trend chart container using mock data."""
    st.subheader(t("price_trend_chart"))
    with st.container(border=True):
        trend_data = prepare_price_trend_data(trends)
        if px is None:
            st.warning(t("plotly_missing"))
            st.dataframe(trend_data, use_container_width=True, hide_index=True)
            return

        chart = px.line(
            trend_data,
            x="Date",
            y="Price",
            color="Crop",
            markers=False,
            custom_data=["Crop", "Formatted Price"],
            labels={"Price": t("modal_price"), "Date": t("date"), "Crop": t("crop")},
        )
        chart.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Date: %{x|%d %b %Y}<br>"
                "Price: %{customdata[1]}<extra></extra>"
            )
        )
        chart.update_layout(
            hovermode="x unified",
            legend_title_text="Crop",
            margin={"l": 10, "r": 10, "t": 20, "b": 10},
            xaxis={
                "rangeselector": {
                    "buttons": [
                        {"count": 7, "label": "1W", "step": "day", "stepmode": "backward"},
                        {"count": 1, "label": "1M", "step": "month", "stepmode": "backward"},
                        {"count": 6, "label": "6M", "step": "month", "stepmode": "backward"},
                        {"count": 1, "label": "1Y", "step": "year", "stepmode": "backward"},
                    ]
                },
                "rangeslider": {"visible": True},
                "type": "date",
            },
            yaxis_tickprefix="₹",
            yaxis_tickformat=",",
        )
        st.plotly_chart(chart, use_container_width=True)
        st.caption(t("market_trend_caption"))


def render_market_table(filtered_prices: pd.DataFrame) -> None:
    """Render local market price table."""
    st.subheader(t("local_market_prices"))
    with st.container(border=True):
        csv_data = filtered_prices.to_csv(index=False).encode("utf-8")
        st.download_button(
            t("download_csv"),
            data=csv_data,
            file_name="farmwise_market_prices.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.dataframe(
            filtered_prices,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Commodity": st.column_config.TextColumn(t("commodity")),
                "Category": st.column_config.TextColumn(t("category")),
                "Market": st.column_config.TextColumn(t("local_market")),
                "Min Price": st.column_config.NumberColumn(t("min_price"), format="₹%d"),
                "Max Price": st.column_config.NumberColumn(t("max_price"), format="₹%d"),
                "Modal Price": st.column_config.NumberColumn(t("price"), format="₹%d"),
                "Trend": st.column_config.TextColumn(t("trend")),
            },
        )


def render_market_page() -> None:
    """Render the complete market trends page."""
    render_sidebar()
    market_data = get_mock_market_data()
    search_query, category = render_filters(market_data)
    filtered_prices = filter_market_prices(market_data["prices"], search_query, category)

    st.divider()
    render_summary_metrics(filtered_prices)

    st.divider()
    render_price_trend_chart(market_data["trends"])

    st.divider()
    render_market_table(filtered_prices)


render_market_page()
