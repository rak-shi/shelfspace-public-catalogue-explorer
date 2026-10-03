# Shelfspace — Public Catalogue Explorer

A small API reverse-engineering project with a custom editorial-style UI. It reads public pages from Books to Scrape, a practice catalogue designed for scraping exercises. No login, private data, or access-control bypass is involved.

## Start-to-finish setup (Windows)

1. Install Python 3.11 or 3.12 and VS Code.
2. Extract this ZIP and open the `shelfspace-project` folder in VS Code.
3. Open a terminal and create a virtual environment:
   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If Python 3.11 is unavailable, replace it with `py -3.12`.
4. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Start the backend in Terminal 1:
   ```powershell
   uvicorn api.main:app --reload
   ```
6. Check `http://127.0.0.1:8000/health` and open interactive API docs at `http://127.0.0.1:8000/docs`.
7. Open a second terminal, activate `.venv`, then start the UI:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   streamlit run dashboard.py
   ```
8. Open the local Streamlit URL (normally `http://localhost:8501`).
9. Run tests:
   ```powershell
   pytest -v
   ```
10. Try `/products?page=1`, `/search?q=history`, browse the dashboard, inspect API JSON, and export CSV. Run everything yourself before saying it works in your submission.

## API routes

- `GET /health` — service health.
- `GET /products?page=1` — normalized product data from one of three bounded catalogue pages.
- `GET /search?q=history` — searches titles across up to three public pages.
- `/docs` — generated API documentation.

## Design choices

The UI is deliberately not a generic admin dashboard. It uses a warm paper background, deep green hero banner, editorial serif heading, catalogue cards, simple browse/search modes, direct source links, a raw-data expander, and CSV export. The UI calls the FastAPI service rather than scraping independently, so the data path is easy to explain.

## Limitations

- HTML selectors can break when the source page layout changes.
- Search is limited to three pages and may miss results elsewhere.
- There is no persistent cache/database, authentication, production rate limiter, or monitoring.
- Upstream availability and content are not guaranteed.
- This is a local educational demo, not a production data service.

## Long-term fix

Prefer an official API, export, or licensed feed and obtain permission for the intended use. If none exists, request a documented integration from the data owner. For production, add a persistent database, scheduled refresh, caching, rate limits, authentication, monitoring, schema validation, and API versioning. Follow site terms and robots guidance, keep request rates low, and stop if access is disallowed.

## Architecture

Browser → Streamlit dashboard → FastAPI → BeautifulSoup/HTTPX source adapter → public practice catalogue.

## Interview explanation

“I chose a public practice catalogue and created a small API that converts its HTML into normalized JSON. The frontend calls the API rather than scraping directly, and the API validates inputs and bounds page access. I added a custom catalogue-style interface and tests for health and input validation. For production, I would replace HTML scraping with an official API or licensed feed and add caching, monitoring, authentication, and rate limiting.”
