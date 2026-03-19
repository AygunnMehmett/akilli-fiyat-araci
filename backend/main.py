from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import quote_plus

from sample_data import get_sample_products, normalize_name

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_search_url(store: str, product_name: str):
    q = quote_plus(product_name)

    if store == "Amazon TR":
        return f"https://www.amazon.com.tr/s?k={q}"
    elif store == "Teknosa":
        return f"https://www.teknosa.com/arama?q={q}"
    elif store == "MediaMarkt":
        return f"https://www.mediamarkt.com.tr/tr/search.html?query={q}"

    return "#"


@app.get("/")
def home():
    return {"status": "API çalışıyor"}


@app.get("/search")
def search(q: str):
    results = get_sample_products(q)

    grouped = {}

    for item in results:
        normalized = normalize_name(item["title"])

        if normalized not in grouped:
            grouped[normalized] = {
                "id": len(grouped) + 1,
                "product": normalized,
                "offers": []
            }

        grouped[normalized]["offers"].append({
            "store": item["store"],
            "price": item["price"],
            "url": item["url"]
        })

    output = []

    for product in grouped.values():
        for offer in product["offers"]:
            output.append({
                "id": product["id"],
                "product": product["product"],
                "store": offer["store"],
                "price": offer["price"],
                "url": offer["url"]
            })

    best_price = min([x["price"] for x in output]) if output else None

    return {
        "query": q,
        "count": len(output),
        "best_price": best_price,
        "results": sorted(output, key=lambda x: x["price"])
    }


@app.get("/products/{product_id}")
def get_product_detail(product_id: int):
    products = {
        1: {
            "id": 1,
            "name": "logitech g305 mouse",
            "best_price": 1249.0,
            "offers": [
                {
                    "store": "MediaMarkt",
                    "price": 1249.0,
                    "url": build_search_url("MediaMarkt", "Logitech G305 Mouse")
                },
                {
                    "store": "Amazon TR",
                    "price": 1299.9,
                    "url": build_search_url("Amazon TR", "Logitech G305 Mouse")
                },
                {
                    "store": "Teknosa",
                    "price": 1349.0,
                    "url": build_search_url("Teknosa", "Logitech G305 Mouse")
                }
            ]
        }
    }

    return products.get(product_id, {"error": "Ürün bulunamadı"})