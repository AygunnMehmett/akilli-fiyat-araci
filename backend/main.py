import sys
import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scraper.sample_data import get_sample_products, normalize_name
from backend.db.database import engine, Base, get_db
from backend.db.models import Product, Offer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"status": "API çalışıyor"}

@app.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    results = get_sample_products(q)

    for item in results:
        normalized = normalize_name(item["title"])

        product = db.query(Product).filter(
            Product.name == normalized
        ).first()

        if not product:
            product = Product(name=normalized)
            db.add(product)
            db.commit()
            db.refresh(product)

        existing_offer = db.query(Offer).filter(
            Offer.product_id == product.id,
            Offer.store == item["store"]
        ).first()

        if not existing_offer:
            offer = Offer(
                product_id=product.id,
                store=item["store"],
                price=item["price"],
                url=item["url"]
            )
            db.add(offer)

    db.commit()

    products = db.query(Product).filter(
        Product.name.ilike(f"%{q}%")
    ).all()

    output = []

    for product in products:
        for offer in product.offers:
            output.append({
                "id": product.id,
    "product": product.name,
    "store": offer.store,
    "price": offer.price,
    "url": offer.url
            })

    best_price = min([x["price"] for x in output]) if output else None

    return {
        "query": q,
        "count": len(output),
        "best_price": best_price,
        "results": sorted(output, key=lambda x: x["price"])
    }

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    return [
        {
            "id": p.id,
            "name": p.name,
            "offers": [
                {
                    "store": o.store,
                    "price": o.price,
                    "url": o.url
                }
                for o in p.offers
            ]
        }
        for p in products
    ]
@app.get("/products/{product_id}")
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"error": "Ürün bulunamadı"}

    offers = [
        {
            "store": o.store,
            "price": o.price,
            "url": o.url
        }
        for o in sorted(product.offers, key=lambda x: x.price)
    ]

    best_price = offers[0]["price"] if offers else None

    return {
        "id": product.id,
        "name": product.name,
        "best_price": best_price,
        "offers": offers
    }