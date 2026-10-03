# Shelfspace — Public Catalogue Explorer

A lightweight REST API that extracts publicly accessible book catalogue information from [Books to Scrape](https://books.toscrape.com/) and exposes it as structured JSON through FastAPI. The project also includes a Streamlit dashboard for browsing, searching, and exporting catalogue data.

Built as a demonstration of website reverse-engineering, HTML parsing, API design, input validation, and automated testing.

## Overview

Many websites display information in HTML pages rather than providing a convenient API for developers. This project demonstrates how publicly accessible catalogue pages can be parsed and exposed through a simple REST API.

### Key Features

- Extract catalogue information from publicly accessible HTML pages.
- Expose book information through REST API endpoints.
- Search for books by title.
- Support pagination for catalogue browsing.
- Validate request parameters and handle upstream failures.
- Browse results through a Streamlit dashboard.
- Export catalogue results to CSV.
- Test API behavior with pytest.

## Tech Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| API framework | FastAPI |
| HTTP requests | HTTPX |
| HTML parsing | BeautifulSoup4 |
| Interactive dashboard | Streamlit |
| Data export | Pandas |
| Automated testing | Pytest |
| API documentation | Swagger UI |

## Architecture

```text
Books to Scrape
      |
      | HTTP request
      v
HTTPX + BeautifulSoup
      |
      | Parse HTML into structured data
      v
FastAPI
      |
      +---- GET /health
      |
      +---- GET /products
      |
      +---- GET /search
      |
      v
JSON responses
      |
      v
Streamlit Dashboard
      |
      +---- Browse and search
      +---- Filter and sort
      +---- Export CSV
```

## Project Structure

```text
shelfspace-public-catalogue-explorer/
├── api/
│   └── main.py          # API endpoints and HTML parsing
├── tests/
│   └── test_api.py      # Automated API tests
├── dashboard.py         # Streamlit dashboard
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment configuration
├── .gitignore           # Excluded files
└── README.md            # Project documentation
```

## Requirements

- Python 3.11 or newer
- Internet connectivity to access the source catalogue
- pip
- Git (optional, for cloning the repository)

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/rak-shi/shelfspace-public-catalogue-explorer.git
cd shelfspace-public-catalogue-explorer
```

Alternatively, download the repository as a ZIP file and extract it.

### 2. Create a virtual environment

**Windows — Command Prompt**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If the dashboard uses Pandas or Requests, make sure those packages are included in `requirements.txt`.

## Running the Application

### Start the API server

From the project root, run:

```bash
uvicorn api.main:app --reload
```

The API will be available at:

- API base URL: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs
- Alternative documentation: http://127.0.0.1:8000/redoc

### Start the dashboard

Open a second terminal, activate the same virtual environment, and run:

```bash
streamlit run dashboard.py
```

Streamlit will display the local dashboard URL in the terminal, usually http://localhost:8501.

## API Reference

The following endpoints are implemented in the project.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API availability |
| GET | `/products?page=1` | Retrieve products from a catalogue page |
| GET | `/search?q=python` | Search catalogue items |

### 1. Health Check

**Request**

```http
GET /health
```

Checks whether the API process is responding.

### 2. Browse Products

**Request**

```http
GET /products?page=1
```

Returns the products parsed from the requested catalogue page.

The response contains structured product information, including fields such as:

- `title` — product title
- `price` — displayed price
- `availability` — displayed stock status
- `rating` — displayed rating
- `product_url` — source product page
- `image_url` — product image location

The exact response structure depends on the implementation in `api/main.py`.

**Example using curl**

```bash
curl "http://127.0.0.1:8000/products?page=1"
```

### 3. Search Products

**Request**

```http
GET /search?q=python
```

Searches the catalogue pages supported by the current implementation and returns matching products.

**Example using curl**

```bash
curl "http://127.0.0.1:8000/search?q=python"
```

The search is limited to the pages scanned by the application; it does not search an unlimited catalogue.

## Testing

The project includes pytest tests for basic API behavior, including the health endpoint and invalid search or pagination parameters.

Run the tests from the project root:

```bash
python -m pytest -v
```

The tests help verify that:

- The health endpoint responds as expected.
- Search requests with invalid short queries are rejected.
- Invalid pagination parameters are rejected.

These tests cover basic behavior. They do not establish complete integration reliability against every possible change or failure on the source website.

## Error Handling

The API validates request parameters before processing them. Invalid input should produce an appropriate client error, while upstream website or network failures may produce a gateway error.

Potential failure cases include:

- The source website is unavailable.
- An HTTP request times out.
- The website changes its HTML markup.
- A requested catalogue page cannot be retrieved.
- The source website limits or rejects requests.

## Assumptions

- The source catalogue is publicly accessible.
- The application only reads publicly displayed catalogue information.
- Product details are extracted from HTML rather than a private or undocumented endpoint.
- The implementation supports only the pagination and search scope defined in the code.
- The source website remains reachable and retains sufficiently compatible HTML markup.

## Limitations

### 1. Dependency on HTML structure

The parser depends on the source website's HTML elements and CSS selectors. A layout change may cause fields to be missing or extracted incorrectly.

### 2. Limited search coverage

Search is restricted to the catalogue pages scanned by the current implementation. A matching item on another page may not be returned.

### 3. Network dependency

Results depend on the source website's availability and response time. Temporary network problems can interrupt requests.

### 4. Rate limits and responsible access

Repeated requests may be restricted by the source website. This project is a demonstration, not a high-volume scraping service.

### 5. No persistent data store

The application retrieves information from the source website when requests are made; it is not designed as a persistent catalogue database.

### 6. Testing scope

The automated tests validate selected API behaviors. More integration tests, parser fixtures, timeout tests, and upstream failure tests would be needed before production deployment.

## Appropriate Long-Term Fix

The preferred long-term solution is to use an official, documented API or an authorized data feed provided by the website owner.

If no official API is available and the owner permits automated access, a production implementation should include:

- Respectful request rates and appropriate timeouts.
- Retry policies with bounded attempts and backoff.
- Caching to avoid unnecessary repeated requests.
- Structured logging and monitoring.
- Parser tests using saved, non-sensitive HTML fixtures.
- Validation for missing or changed fields.
- Clear handling of upstream errors and partial results.
- Compliance with the website's terms of use and applicable access rules.

The application should not bypass access controls, evade rate limits, or collect private information.

## Security and Privacy

- No customer records or private data are required.
- No API keys or credentials are required for the basic workflow.
- The application reads publicly accessible catalogue pages.
- Do not commit credentials, local environment files containing secrets, or virtual-environment folders to GitHub.

## Future Improvements

- Add integration tests with mocked upstream responses.
- Improve handling of timeouts and temporary upstream failures.
- Add caching and configurable request timeouts.
- Expand search coverage with responsible pagination.
- Add response schemas and consistent error messages.
- Add automated CI testing.
- Add screenshots and example API responses to the documentation.

## Author

**Rakshitha Valipireddy**

- GitHub: https://github.com/rak-shi
- Project repository: https://github.com/rak-shi/shelfspace-public-catalogue-explorer

---

*This project is an educational demonstration of HTML parsing and REST API development using a public practice catalogue. It is not an official API or an affiliated service of Books to Scrape.*
