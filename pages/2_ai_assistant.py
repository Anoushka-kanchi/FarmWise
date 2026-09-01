from pathlib import Path

import streamlit as st

from ui_theme import inject_global_theme, render_hero_image
from utils.helpers import get_ai_response, get_crop_recommendation, render_integration_badges
from utils.translations import render_language_selector, t


st.set_page_config(
    page_title="AI Assistant | Smart Farming Platform",
    page_icon="🤖",
    layout="wide",
)

inject_global_theme()


# Temporary mock AI responses. Person 2 can replace these interfaces with
# model/API utilities while keeping the Streamlit UI functions unchanged.
QUICK_PROMPTS = [
    "quick_prompt_soil",
    "quick_prompt_tomato",
    "quick_prompt_irrigation",
    "quick_prompt_rain",
]

BASE_DIR = Path(__file__).resolve().parent.parent


def initialize_chat_history() -> None:
    """Create chat history state when the page first loads."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": t("chat_welcome"),
            }
        ]


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
    """Render AI assistant page navigation."""
    with st.sidebar:
        st.title("🌱 FarmWise")
        st.caption(t("ai_assistant_caption"))

        st.divider()
        st.subheader(t("global_controls"))
        render_language_selector("language_selector_ai")
        st.divider()

        st.page_link("app.py", label=t("home"), icon="🏠")
        st.page_link("pages/1_dashboard.py", label=t("dashboard"), icon="📊")
        st.page_link("pages/2_ai_assistant.py", label=t("ai_assistant"), icon="🤖")
        render_optional_page_link("pages/3_weather.py", t("weather"), "⛅")
        render_optional_page_link("pages/4_market.py", t("market_trends"), "📈")
        render_optional_page_link("pages/5_marketplace.py", t("marketplace"), "🛒")

        st.divider()

        if st.button(t("clear_chat"), use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": t("chat_cleared"),
                }
            ]
            st.rerun()

        st.divider()
        render_integration_badges()


def append_chat_exchange(user_prompt: str) -> None:
    """Append a user prompt and mock assistant response to chat history."""
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.session_state.messages.append(
        {"role": "assistant", "content": get_ai_response(user_prompt)}
    )


def render_quick_prompts() -> None:
    """Render quick prompt buttons for common farming queries."""
    st.subheader(t("quick_prompts"))
    prompt_columns = st.columns(2)

    for index, prompt_key in enumerate(QUICK_PROMPTS):
        prompt = t(prompt_key)
        with prompt_columns[index % 2]:
            if st.button(prompt, key=f"quick_prompt_{index}", use_container_width=True):
                append_chat_exchange(prompt)
                st.rerun()


def render_chat_messages() -> None:
    """Render the current chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


def render_chatbot_tab() -> None:
    """Render the Farming AI Chatbot tab."""
    render_quick_prompts()
    st.divider()
    render_chat_messages()

    user_prompt = st.chat_input(t("ask_farming_question"))
    if user_prompt:
        append_chat_exchange(user_prompt)
        st.rerun()


def render_crop_recommendation_tab() -> None:
    """Render crop recommendation form and result container."""
    with st.form("crop_recommendation_form"):
        st.subheader(t("crop_recommendation_inputs"))

        soil_col_1, soil_col_2, soil_col_3 = st.columns(3)
        nitrogen = soil_col_1.number_input(t("nitrogen"), min_value=0.0, max_value=200.0, value=65.0, step=1.0)
        phosphorus = soil_col_2.number_input(t("phosphorus"), min_value=0.0, max_value=200.0, value=45.0, step=1.0)
        potassium = soil_col_3.number_input(t("potassium"), min_value=0.0, max_value=200.0, value=55.0, step=1.0)

        climate_col_1, climate_col_2, climate_col_3 = st.columns(3)
        rainfall = climate_col_1.number_input(t("rainfall"), min_value=0.0, max_value=3000.0, value=720.0, step=10.0)
        temperature = climate_col_2.number_input(t("temperature"), min_value=0.0, max_value=60.0, value=28.0, step=0.5)
        ph = climate_col_3.number_input(t("soil_ph"), min_value=0.0, max_value=14.0, value=6.8, step=0.1)

        submitted = st.form_submit_button(t("predict_best_crop"), type="primary", use_container_width=True)

    if submitted:
        recommendation = get_crop_recommendation(
            {
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "rainfall": rainfall,
                "temperature": temperature,
                "ph": ph,
            }
        )

        with st.container(border=True):
            st.success(t("recommendation_generated"))
            result_col, detail_col = st.columns([1, 2], gap="large")
            result_col.metric(t("best_crop"), recommendation["crop"], recommendation["confidence"])
            detail_col.write(f"**{t('why')}:** {recommendation['reason']}")
            detail_col.info(recommendation["next_step"])


def render_ai_assistant_page() -> None:
    """Render the complete AI assistant page."""
    initialize_chat_history()
    render_sidebar()

    render_hero_image(
        t("ai_assistant"),
        t("ai_assistant_intro"),
        "https://images.unsplash.com/photo-1581090464777-f3220bbe1b8b?auto=format&fit=crop&w=1600&q=80",
    )
    st.title(t("ai_assistant"))
    st.write(t("ai_assistant_intro"))

    chatbot_tab, recommendation_tab = st.tabs([t("farming_ai_chatbot"), t("crop_recommendation")])

    with chatbot_tab:
        render_chatbot_tab()

    with recommendation_tab:
        render_crop_recommendation_tab()


render_ai_assistant_page()
