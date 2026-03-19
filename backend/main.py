import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.sample_data import get_sample_products, normalize_name

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
                    "url": "https://example.com/mediamarkt-g305"
                },
                {
                    "store": "Amazon TR",
                    "price": 1299.9,
                    "url": "https://example.com/amazon-g305"
                },
                {
                    "store": "Teknosa",
                    "price": 1349.0,
                    "url": "https://example.com/teknosa-g305"
                }
            ]
        }
    }

    return products.get(product_id, {"error": "Ürün bulunamadı"})