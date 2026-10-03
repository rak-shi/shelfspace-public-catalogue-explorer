
import html
import re

import pandas as pd
import requests
import streamlit as st

# --------------------------------------------------
# Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Shelfspace | Book Explorer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

API = "http://127.0.0.1:8000"
SOURCE_NAME = "Books to Scrape"

# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background-color: #F7F5EF;
        color: #203A33;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1320px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main text contrast */
    [data-testid="stAppViewContainer"] .main h1,
    [data-testid="stAppViewContainer"] .main h2,
    [data-testid="stAppViewContainer"] .main h3,
    [data-testid="stAppViewContainer"] .main p,
    [data-testid="stAppViewContainer"] .main label,
    [data-testid="stAppViewContainer"] .main
        [data-testid="stMetricLabel"],
    [data-testid="stAppViewContainer"] .main
        [data-testid="stMetricValue"] {
        color: #203A33;
    }

    /* Hero section */
    .ss-hero {
        background: linear-gradient(135deg, #183B31, #31594A);
        padding: 34px 38px;
        border-radius: 22px;
        margin-bottom: 28px;
        border: 1px solid #416956;
    }

    .ss-eyebrow {
        color: #D7E5C7;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .ss-hero h1 {
        color: #FFF9ED !important;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(2.5rem, 5vw, 4rem);
        line-height: 1.1;
        margin: 0 0 12px 0;
    }

    .ss-hero p {
        color: #E3EADF !important;
        font-size: 1.05rem;
        margin: 0;
        max-width: 650px;
        line-height: 1.7;
    }

    .ss-hero-tag {
        display: inline-block;
        margin-top: 22px;
        padding: 7px 12px;
        border: 1px solid #71917B;
        border-radius: 30px;
        color: #F5F4E8;
        font-size: 0.78rem;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E6E0D5;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 3px 12px rgba(32, 58, 51, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: #69756B !important;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #203A33 !important;
        font-weight: 700;
    }

    /* Book cards */
    .book-card {
        background: #FFFFFF;
        border: 1px solid #E5DFD3;
        border-radius: 17px;
        padding: 18px;
        margin-bottom: 8px;
        min-height: 355px;
        box-shadow: 0 4px 14px rgba(32, 58, 51, 0.04);
        transition: transform 0.2s ease,
                    box-shadow 0.2s ease;
        overflow-wrap: anywhere;
    }

    .book-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 9px 24px rgba(32, 58, 51, 0.10);
    }

    .book-cover-wrap {
        height: 175px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #F7F5EF;
        border-radius: 11px;
        margin-bottom: 17px;
        padding: 10px;
    }

    .book-cover {
        max-height: 155px;
        max-width: 100%;
        object-fit: contain;
    }

    .book-cover-placeholder {
        color: #829184;
        font-size: 2.5rem;
    }

    .book-title {
        color: #203A33;
        font-size: 1rem;
        font-weight: 700;
        line-height: 1.5;
        min-height: 72px;
        margin-bottom: 9px;
    }

    .book-rating {
        color: #9A6B24;
        font-size: 0.9rem;
        margin-bottom: 10px;
    }

    .book-price {
        color: #A95135;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .book-stock {
        display: inline-block;
        background: #E8F3E8;
        color: #28613D;
        border-radius: 30px;
        padding: 5px 9px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 13px;
    }

    .book-link {
        display: block;
        color: #FFFFFF !important;
        background: #24483D;
        text-align: center;
        text-decoration: none !important;
        padding: 10px 12px;
        border-radius: 9px;
        font-size: 0.86rem;
        font-weight: 700;
        margin-top: 3px;
    }

    .book-link:hover {
        background: #356653;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #20312C;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stCaption {
        color: #F5F3E9;
    }

    [data-testid="stSidebar"] hr {
        border-color: #53675D;
    }

    /* Inputs and buttons */
    .stTextInput input {
        border-radius: 10px;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    .stButton > button {
        background: #24483D;
        color: #FFFFFF;
        border: 1px solid #24483D;
    }

    .stButton > button:hover {
        background: #356653;
        border-color: #356653;
        color: #FFFFFF;
    }

    /* Footer */
    .ss-footer {
        color: #70796F;
        font-size: 0.82rem;
        text-align: center;
        padding: 20px 0 4px 0;
        line-height: 1.8;
    }

    hr {
        border-color: #E1DCCF;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <section class="ss-hero">
        <div class="ss-eyebrow">Public Catalogue Lab</div>
        <h1>Shelfspace</h1>
        <p>
            A thoughtful space to discover books, explore catalogue
            data, and experience a simple API-powered application.
        </p>
        <span class="ss-hero-tag">
            Python · FastAPI · Streamlit
        </span>
    </section>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 📚 Reading desk")
    st.caption("Your personal catalogue explorer")

    mode = st.radio(
        "Choose a view",
        ["Browse shelves", "Find a title"],
        index=0,
    )

    st.divider()
    st.markdown("### Refine your results")

    min_rating = st.selectbox(
        "Minimum rating",
        ["Any rating", "2+ stars", "3+ stars", "4+ stars", "5 stars"],
        index=0,
    )

    in_stock_only = st.checkbox(
        "Show books in stock only",
        value=False,
    )

    sort_by = st.selectbox(
        "Sort results",
        [
            "Default order",
            "Title: A–Z",
            "Title: Z–A",
            "Price: low to high",
            "Price: high to low",
            "Rating: high to low",
        ],
    )

    st.divider()
    st.markdown("### About this project")
    st.caption(f"Catalogue source: {SOURCE_NAME}")
    st.caption("Educational project using public pages.")
    st.caption("No login or private account data is accessed.")

# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def fetch_items(endpoint, params=None, timeout=20):
    """Fetch and validate a response from the local API."""
    response = requests.get(
        f"{API}{endpoint}",
        params=params,
        timeout=timeout,
    )
    response.raise_for_status()

    payload = response.json()
    items = payload.get("items", [])

    if not isinstance(items, list):
        raise ValueError("The API returned an unexpected product format.")

    return items


def price_as_number(value):
    """Convert a displayed price such as £12.84 to a number."""
    try:
        cleaned = re.sub(r"[^0-9.]", "", str(value))
        return float(cleaned) if cleaned else float("inf")
    except (ValueError, TypeError):
        return float("inf")


def rating_as_number(value):
    try:
        return int(value or 0)
    except (ValueError, TypeError):
        return 0


def render_book_card(book):
    """Render a catalogue item as a styled HTML card."""
    title = html.escape(str(book.get("title") or "Untitled book"))
    price = html.escape(str(book.get("price") or "Price unavailable"))
    availability = str(book.get("availability") or "Availability unknown")
    rating = rating_as_number(book.get("rating"))
    product_url = str(book.get("product_url") or "#")
    image_url = book.get("image_url")

    safe_product_url = html.escape(product_url, quote=True)

    if image_url:
        safe_image_url = html.escape(str(image_url), quote=True)
        cover_html = (
            f'<img class="book-cover" src="{safe_image_url}" '
            f'alt="{title}" loading="lazy">'
        )
    else:
        cover_html = '<div class="book-cover-placeholder">📖</div>'

    rating_text = "★" * rating + "☆" * max(0, 5 - rating)
    rating_label = f"{rating}/5" if rating else "Not rated"

    in_stock = "in stock" in availability.casefold()
    stock_class = "book-stock" if in_stock else "book-stock"
    safe_availability = html.escape(availability)

    st.markdown(
        f"""
        <article class="book-card">
            <div class="book-cover-wrap">
                {cover_html}
            </div>
            <div class="book-title">{title}</div>
            <div class="book-rating"
                 title="{html.escape(rating_label)}">
                {rating_text}
                <span style="color:#73796F;font-size:0.78rem">
                    {html.escape(rating_label)}
                </span>
            </div>
            <div class="book-price">{price}</div>
            <div class="{stock_class}">
                {safe_availability}
            </div>
            <a class="book-link"
               href="{safe_product_url}"
               target="_blank"
               rel="noopener noreferrer">
                View book ↗
            </a>
        </article>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# API health check
# --------------------------------------------------

api_connected = False

try:
    health_response = requests.get(
        f"{API}/health",
        timeout=3,
    )
    health_response.raise_for_status()
    api_connected = health_response.json().get("status") == "ok"
except (requests.RequestException, ValueError):
    api_connected = False

# --------------------------------------------------
# Browse or search
# --------------------------------------------------

items = []
page = None
query = ""

try:
    if mode == "Browse shelves":
        st.markdown("### Explore the shelves")
        st.write(
            "Browse books from the selected catalogue page."
        )

        page = st.selectbox(
            "Choose a catalogue page",
            options=[1, 2, 3],
            format_func=lambda number: f"Shelf {number}",
        )

        items = fetch_items(
            "/products",
            params={"page": page},
        )

    else:
        st.markdown("### Find your next read")
        st.write(
            "Search book titles using a word or phrase."
        )

        query = st.text_input(
            "Search book titles",
            placeholder="Try: history, love, or mystery",
            max_chars=80,
        )

        if len(query.strip()) < 2:
            st.info(
                "Enter at least two characters to search the catalogue."
            )
        else:
            with st.spinner("Searching the public catalogue..."):
                items = fetch_items(
                    "/search",
                    params={"q": query.strip()},
                    timeout=45,
                )

    # --------------------------------------------------
    # Filter and sort
    # --------------------------------------------------

    if min_rating != "Any rating":
        required_rating = int(min_rating[0])
        items = [
            book for book in items
            if rating_as_number(book.get("rating")) >= required_rating
        ]

    if in_stock_only:
        items = [
            book for book in items
            if "in stock" in str(
                book.get("availability", "")
            ).casefold()
        ]

    if sort_by == "Title: A–Z":
        items.sort(
            key=lambda book: str(book.get("title", "")).casefold()
        )

    elif sort_by == "Title: Z–A":
        items.sort(
            key=lambda book: str(book.get("title", "")).casefold(),
            reverse=True,
        )

    elif sort_by == "Price: low to high":
        items.sort(
            key=lambda book: price_as_number(book.get("price"))
        )

    elif sort_by == "Price: high to low":
        items.sort(
            key=lambda book: price_as_number(book.get("price")),
            reverse=True,
        )

    elif sort_by == "Rating: high to low":
        items.sort(
            key=lambda book: rating_as_number(book.get("rating")),
            reverse=True,
        )

    # --------------------------------------------------
    # Summary metrics
    # --------------------------------------------------

    st.markdown("")

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Books in this view",
        len(items),
    )

    metric2.metric(
        "Catalogue page",
        str(page) if page is not None else "Search",
    )

    metric3.metric(
        "API status",
        "Connected" if api_connected else "Offline",
        delta="Healthy" if api_connected else "Check backend",
        delta_color="normal" if api_connected else "inverse",
    )

    st.divider()

    # --------------------------------------------------
    # Catalogue cards
    # --------------------------------------------------

    st.markdown("### Your catalogue")

    if items:
        st.caption(
            f"Showing {len(items)} book(s). "
            "Select a book's source link to open its catalogue page."
        )

        card_columns = st.columns(3, gap="large")

        for index, book in enumerate(items):
            with card_columns[index % 3]:
                render_book_card(book)

        # --------------------------------------------------
        # Export and inspect
        # --------------------------------------------------

        st.divider()
        st.markdown("### Catalogue data")

        export_df = pd.DataFrame(items)

        csv_data = export_df.to_csv(
            index=False,
            encoding="utf-8-sig",
        ).encode("utf-8-sig")

        left, right = st.columns([1, 2])

        with left:
            st.download_button(
                label="⬇ Export results as CSV",
                data=csv_data,
                file_name="shelfspace_catalogue.csv",
                mime="text/csv",
                width="stretch",
            )

        with right:
            st.caption(
                "Export the currently filtered and sorted results "
                "for further analysis."
            )

        with st.expander("Inspect structured API data"):
            st.dataframe(
                export_df,
                width="stretch",
                hide_index=True,
            )

    elif mode == "Find a title" and len(query.strip()) < 2:
        pass

    else:
        st.info(
            "No books match the current filters. "
            "Try another search term or relax your filters."
        )

except requests.HTTPError as exc:
    status_code = (
        exc.response.status_code
        if exc.response is not None
        else "unknown"
    )

    st.error(
        f"The catalogue API returned HTTP {status_code}. "
        "Please try again or inspect the API documentation."
    )

except requests.RequestException:
    st.error(
        "Cannot connect to the Shelfspace API. "
        "Start the backend in a separate terminal using:"
    )
    st.code("uvicorn api.main:app --reload")

except (ValueError, KeyError, TypeError) as exc:
    st.error(
        "The API response could not be processed. "
        "Check the backend response and try again."
    )
    with st.expander("Technical details"):
        st.code(str(exc))

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="ss-footer">
        <strong>Shelfspace</strong> · Public Catalogue Explorer<br>
        Built with Python, FastAPI, HTTPX, BeautifulSoup and Streamlit.<br>
        Educational demonstration using public catalogue pages.
        For production integrations, prefer an official API or
        a licensed data feed where available.
    </div>
    """,
    unsafe_allow_html=True,
)
