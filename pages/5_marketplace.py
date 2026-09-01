from pathlib import Path

import pandas as pd
import streamlit as st

from ui_theme import inject_global_theme, render_hero_image
from utils.helpers import add_product, create_order, get_products, render_integration_badges
from utils.translations import render_language_selector, t


st.set_page_config(
    page_title="Marketplace | Smart Farming Platform",
    page_icon="🛒",
    layout="wide",
)

inject_global_theme()


# Temporary mock marketplace data. Person 3 or Person 4 can replace
# get_mock_marketplace_products() with API/database results later.
MOCK_CATEGORIES = ["All", "Seeds", "Fertilizers", "Equipment", "Produce"]
QUICK_CATEGORY_FILTERS = ["All Products", "Seeds", "Fertilizers", "Equipment", "Produce"]
CATEGORY_LABEL_KEYS = {
    "All": "all",
    "All Products": "all_products",
    "Seeds": "seeds",
    "Fertilizers": "fertilizers",
    "Equipment": "equipment",
    "Produce": "produce",
}

MOCK_PRODUCTS = [
    {
        "id": "seed-tomato-001",
        "title": "Hybrid Tomato Seeds",
        "category": "Seeds",
        "price": 420,
        "unit": "250 g pack",
        "seller": "GreenGrow Supplies",
        "image": "https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?auto=format&fit=crop&w=900&q=80",
        "description": "High-germination tomato seeds suitable for protected and open-field farming.",
    },
    {
        "id": "fert-organic-002",
        "title": "Organic Compost",
        "category": "Fertilizers",
        "price": 680,
        "unit": "50 kg bag",
        "seller": "SoilCare Organics",
        "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?auto=format&fit=crop&w=900&q=80",
        "description": "Nutrient-rich compost for improving soil structure and microbial activity.",
    },
    {
        "id": "equip-sprayer-003",
        "title": "Battery Sprayer",
        "category": "Equipment",
        "price": 2450,
        "unit": "16 L tank",
        "seller": "AgriTools Hub",
        "image": "https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&w=900&q=80",
        "description": "Rechargeable sprayer for fertilizer, pesticide, and foliar application.",
    },
    {
        "id": "produce-onion-004",
        "title": "Fresh Red Onions",
        "category": "Produce",
        "price": 1900,
        "unit": "per quintal",
        "seller": "Nashik Farmer Collective",
        "image": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?auto=format&fit=crop&w=900&q=80",
        "description": "Sorted red onions available for wholesale buyers and local retailers.",
    },
    {
        "id": "seed-wheat-005",
        "title": "Certified Wheat Seeds",
        "category": "Seeds",
        "price": 1250,
        "unit": "40 kg bag",
        "seller": "HarvestLine Agro",
        "image": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=900&q=80",
        "description": "Certified seed variety for reliable crop establishment and uniform growth.",
    },
    {
        "id": "equip-drip-006",
        "title": "Drip Irrigation Kit",
        "category": "Equipment",
        "price": 3600,
        "unit": "1 acre starter kit",
        "seller": "WaterWise Irrigation",
        "image": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=900&q=80",
        "description": "Starter drip kit for efficient water delivery across vegetable rows.",
    },
]

BASE_DIR = Path(__file__).resolve().parent.parent


def get_mock_marketplace_products() -> list[dict]:
    """Return marketplace product listings."""
    return MOCK_PRODUCTS


def normalize_product(product: dict, index: int) -> dict:
    """Normalize database product fields into the marketplace card schema."""
    return {
        "id": str(product.get("id") or product.get("product_id") or f"db-product-{index}"),
        "title": str(product.get("title") or product.get("name") or "Untitled Product"),
        "category": str(product.get("category") or "Produce"),
        "price": float(product.get("price") or 0),
        "unit": str(product.get("unit") or product.get("quantity") or "unit"),
        "seller": str(product.get("seller") or product.get("seller_name") or "FarmWise Seller"),
        "image": str(
            product.get("image")
            or product.get("image_url")
            or "https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?auto=format&fit=crop&w=900&q=80"
        ),
        "description": str(product.get("description") or "No product description available yet."),
    }


def get_marketplace_products() -> list[dict]:
    """Return database products, falling back to mock listings when integration is unavailable."""
    products = get_products()
    if not products:
        return get_mock_marketplace_products()

    return [normalize_product(product, index) for index, product in enumerate(products)]


def get_mock_marketplace_categories() -> list[str]:
    """Return marketplace categories."""
    return MOCK_CATEGORIES


def save_product_listing(product: dict) -> bool:
    """Save a product listing through the database helper when available."""
    return add_product(product)


def initialize_cart() -> None:
    """Create cart state when the page first loads."""
    if "cart" not in st.session_state:
        st.session_state.cart = []

    if not isinstance(st.session_state.cart, list):
        st.session_state.cart = []

    st.session_state.marketplace_cart = st.session_state.cart


def page_available(page_path: str) -> bool:
    """Return whether a target Streamlit page exists."""
    return (BASE_DIR / page_path).exists()


def render_optional_page_link(page_path: str, label: str, icon: str) -> None:
    """Render navigation when a target page exists, or a small placeholder."""
    if page_available(page_path):
        st.page_link(page_path, label=label, icon=icon)
    else:
        st.caption(t("coming_soon", icon=icon, label=label))


def add_to_cart(product: dict) -> None:
    """Add a selected product to session cart state."""
    st.session_state.cart.append(
        {
            "id": product["id"],
            "title": product["title"],
            "price": product["price"],
            "unit": product["unit"],
            "seller": product["seller"],
        }
    )
    st.session_state.marketplace_cart = st.session_state.cart
    st.toast(t("added_to_cart", product=product["title"]), icon="🛒")


def clear_cart() -> None:
    """Clear all selected marketplace items."""
    st.session_state.cart = []
    st.session_state.marketplace_cart = st.session_state.cart


def render_sidebar() -> None:
    """Render marketplace navigation and cart summary."""
    with st.sidebar:
        st.title("🌱 FarmWise")
        st.caption(t("marketplace"))

        st.divider()
        st.subheader(t("global_controls"))
        render_language_selector("language_selector_marketplace")
        st.divider()
        render_integration_badges()
        st.divider()

        st.page_link("app.py", label=t("home"), icon="🏠")
        st.page_link("pages/1_dashboard.py", label=t("dashboard"), icon="📊")
        render_optional_page_link("pages/2_ai_assistant.py", t("ai_assistant"), "🤖")
        st.page_link("pages/3_weather.py", label=t("weather"), icon="⛅")
        st.page_link("pages/4_market.py", label=t("market_trends"), icon="📈")
        st.page_link("pages/5_marketplace.py", label=t("marketplace"), icon="🛒")

        st.divider()
        render_cart_summary()


def render_cart_summary() -> None:
    """Render a sidebar cart summary from session state."""
    cart_items = st.session_state.cart
    cart_total = sum(item["price"] for item in cart_items)

    st.subheader(t("cart"))
    st.metric(t("selected_items"), len(cart_items), f"₹{cart_total:,.0f}")

    if not cart_items:
        st.caption(t("cart_empty"))
        return

    with st.expander(t("cart_view_items"), expanded=True):
        for item in cart_items:
            st.write(f"**{item['title']}**")
            st.caption(f"₹{item['price']:,.0f} • {item['unit']} • {item['seller']}")

        st.button(t("clear_cart"), use_container_width=True, on_click=clear_cart)


def filter_products(products: list[dict], search_query: str, category: str) -> list[dict]:
    """Filter marketplace products by search query and category."""
    filtered_products = products

    if category != "All":
        filtered_products = [
            product for product in filtered_products if product["category"] == category
        ]

    if search_query:
        normalized_query = search_query.lower()
        filtered_products = [
            product
            for product in filtered_products
            if normalized_query in product["title"].lower()
            or normalized_query in product["seller"].lower()
            or normalized_query in product["description"].lower()
        ]

    return filtered_products


def render_marketplace_filters(categories: list[str]) -> tuple[str, str]:
    """Render marketplace search and category filter controls."""
    st.subheader(t("browse_products"))
    category_label = render_quick_category_filter() or "All Products"

    search_query = st.text_input(
        t("marketplace_search"),
        placeholder=t("marketplace_search_placeholder"),
    )
    category = "All" if category_label == "All Products" else category_label

    if category not in categories:
        category = "All"

    return search_query.strip(), category


def render_quick_category_filter() -> str:
    """Render quick category filter pills with a safe fallback."""
    option_labels = [t(CATEGORY_LABEL_KEYS[category]) for category in QUICK_CATEGORY_FILTERS]
    label_to_category = dict(zip(option_labels, QUICK_CATEGORY_FILTERS))

    if hasattr(st, "pills"):
        selected_label = st.pills(t("quick_categories"), option_labels, default=option_labels[0])
        return label_to_category.get(selected_label, "All Products")

    if hasattr(st, "segmented_control"):
        selected_label = st.segmented_control(t("quick_categories"), option_labels, default=option_labels[0])
        return label_to_category.get(selected_label, "All Products")

    selected_label = st.radio(t("quick_categories"), option_labels, horizontal=True)
    return label_to_category.get(selected_label, "All Products")


def render_product_card(product: dict) -> None:
    """Render a single marketplace product card."""
    with st.container(border=True):
        st.image(product["image"], use_container_width=True)
        st.subheader(product["title"])
        st.caption(t(CATEGORY_LABEL_KEYS.get(product["category"], "category")))
        st.metric(t("price"), f"₹{product['price']:,.0f}", product["unit"])
        st.write(f"**{t('seller')}:** {product['seller']}")
        st.write(product["description"])
        st.button(
            t("add_to_cart"),
            key=f"add_to_cart_{product['id']}",
            use_container_width=True,
            on_click=add_to_cart,
            args=(product,),
        )


def render_product_grid(products: list[dict]) -> None:
    """Render marketplace products in a 3-column grid."""
    if not products:
        st.warning(t("no_products"))
        return

    for start_index in range(0, len(products), 3):
        columns = st.columns(3)
        for column, product in zip(columns, products[start_index : start_index + 3]):
            with column:
                render_product_card(product)


def render_browse_tab() -> None:
    """Render the Browse Marketplace tab."""
    products = get_marketplace_products()
    categories = get_mock_marketplace_categories()
    search_query, category = render_marketplace_filters(categories)
    filtered_products = filter_products(products, search_query, category)

    st.caption(t("marketplace_showing", shown=len(filtered_products), total=len(products)))
    render_product_grid(filtered_products)


def render_sell_product_tab() -> None:
    """Render form for submitting new product listings."""
    with st.form("sell_product_form", clear_on_submit=True):
        st.subheader(t("create_product_listing"))

        title = st.text_input(t("title"), placeholder=t("product_title_placeholder"))
        category = st.selectbox(
            t("category"),
            MOCK_CATEGORIES[1:],
            format_func=lambda value: t(CATEGORY_LABEL_KEYS[value]),
        )

        price_col, quantity_col = st.columns(2)
        price = price_col.number_input(t("price"), min_value=0.0, step=10.0, format="%.2f")
        quantity = quantity_col.text_input(t("quantity"), placeholder=t("quantity_placeholder"))

        image = st.file_uploader(t("image_uploader"), type=["png", "jpg", "jpeg"])
        description = st.text_area(
            t("description"),
            placeholder=t("description_placeholder"),
            height=140,
        )

        submitted = st.form_submit_button(t("submit_listing"), type="primary", use_container_width=True)

    if submitted:
        if not title or price <= 0 or not quantity or not description:
            st.warning(t("listing_required"))
            return

        product_payload = {
            "title": title,
            "category": category,
            "price": price,
            "quantity": quantity,
            "image_name": image.name if image is not None else None,
            "description": description,
            "seller": "Current User",
        }

        saved_to_database = save_product_listing(product_payload)

        with st.container(border=True):
            if saved_to_database:
                st.success(t("listing_saved"))
            else:
                st.success(t("listing_submitted_local"))
                st.caption(t("listing_not_persisted"))

            st.write(f"**{t('title')}:** {title}")
            st.write(f"**{t('category')}:** {t(CATEGORY_LABEL_KEYS[category])}")
            st.write(f"**{t('price')}:** ₹{price:,.2f}")
            st.write(f"**{t('quantity')}:** {quantity}")
            if image is not None:
                st.caption(t("uploaded_image", name=image.name))


def render_cart_table(cart_items: list[dict]) -> None:
    """Render a clean shopping cart table."""
    table_data = pd.DataFrame(cart_items)
    if table_data.empty:
        st.caption(t("cart_empty_overlay"))
        return

    table_data = table_data.rename(
        columns={
            "title": t("product"),
            "price": t("price"),
            "unit": t("unit"),
            "seller": t("seller"),
        }
    )[[t("product"), t("price"), t("unit"), t("seller")]]

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            t("price"): st.column_config.NumberColumn(t("price"), format="₹%d"),
        },
    )


def render_cart_popover() -> None:
    """Render the top-right overlay shopping cart."""
    cart_items = st.session_state.cart
    subtotal = sum(item["price"] for item in cart_items)

    if hasattr(st, "popover"):
        with st.popover(t("view_cart"), use_container_width=True):
            render_cart_table(cart_items)
            st.metric(t("subtotal"), f"₹{subtotal:,.0f}")
            if st.button(t("proceed_to_checkout"), type="primary", use_container_width=True):
                create_order(cart_items)
                st.success(t("checkout_connected_later"))
        return

    with st.expander(t("view_cart")):
        render_cart_table(cart_items)
        st.metric(t("subtotal"), f"₹{subtotal:,.0f}")
        if st.button(t("proceed_to_checkout"), type="primary", use_container_width=True):
            create_order(cart_items)
            st.success(t("checkout_connected_later"))


def render_page_header() -> None:
    """Render marketplace title with cart popover aligned to the right."""
    render_hero_image(
        t("marketplace"),
        t("marketplace_intro"),
        "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=1600&q=80",
    )
    title_col, cart_col = st.columns([3, 1])

    with title_col:
        st.title(t("marketplace"))
        st.write(t("marketplace_intro"))

    with cart_col:
        render_cart_popover()


def render_marketplace_page() -> None:
    """Render the complete marketplace page."""
    initialize_cart()
    render_sidebar()

    render_page_header()

    browse_tab, sell_tab = st.tabs([t("browse_marketplace"), t("sell_product")])

    with browse_tab:
        render_browse_tab()

    with sell_tab:
        render_sell_product_tab()


render_marketplace_page()
