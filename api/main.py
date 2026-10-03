from fastapi import FastAPI, Query, HTTPException
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = FastAPI(title="Shelfspace Public Catalogue API", version="1.0.0")
BASE = "https://books.toscrape.com/"

async def get_page(page: int):
    if page not in (1, 2, 3):
        raise HTTPException(400, "For this demo, page must be 1, 2, or 3.")
    url = BASE if page == 1 else urljoin(BASE, f"catalogue/page-{page}.html")
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            r = await client.get(url, headers={"User-Agent": "Shelfspace-learning-project/1.0"})
            r.raise_for_status()
    except httpx.HTTPError:
        raise HTTPException(502, "The public catalogue is temporarily unavailable.")
    soup = BeautifulSoup(r.text, "html.parser")
    result = []
    ratings = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
    for card in soup.select("article.product_pod"):
        a = card.select_one("h3 a")
        price = card.select_one(".price_color")
        if not a or not price:
            continue
        rating_class = card.select_one(".star-rating")
        rating = next((v for k,v in ratings.items() if rating_class and k in rating_class.get("class", [])), None)
        href = a.get("href", "")
        availability = card.select_one(".availability")
        image = card.select_one("img")
        result.append({
            "id": href.split("/")[-1].replace(".html", ""),
            "title": (a.get("title") or a.get_text(strip=True)),
            "price": price.get_text(strip=True),
            "availability": availability.get_text(" ", strip=True) if availability else "Unknown",
            "rating": rating,
            "product_url": urljoin(url, href),
            "image_url": urljoin(url, image.get("src", "")) if image else None
        })
    return result

@app.get("/health")
def health():
    return {"status": "ok", "service": "Shelfspace"}

@app.get("/products")
async def products(page: int = Query(1, ge=1, le=3)):
    return {"page": page, "source": "Books to Scrape", "items": await get_page(page)}

@app.get("/search")
async def search(q: str = Query(..., min_length=2, max_length=80)):
    matches = []
    for page in (1, 2, 3):
        for item in await get_page(page):
            if q.casefold() in item["title"].casefold():
                matches.append(item)
    return {"query": q, "count": len(matches), "source": "Books to Scrape", "items": matches}
