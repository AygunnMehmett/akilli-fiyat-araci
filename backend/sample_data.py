from urllib.parse import quote_plus


def normalize_name(title: str):
    title = title.lower()
    replacements = [
        "lightspeed",
        "wireless",
        "kablosuz",
        "oyuncu",
        "gaming",
        "siyah"
    ]

    for word in replacements:
        title = title.replace(word, "")

    title = " ".join(title.split())
    return title


def build_search_url(store: str, title: str):
    q = quote_plus(title)

    if store == "Amazon TR":
        return f"https://www.amazon.com.tr/s?k={q}"
    elif store == "Teknosa":
        return f"https://www.teknosa.com/arama?q={q}"
    elif store == "MediaMarkt":
        return f"https://www.mediamarkt.com.tr/tr/search.html?query={q}"

    return "#"


def get_sample_products(query: str):
    query = query.lower()

    raw_products = [
        {
            "store": "Amazon TR",
            "title": "Logitech G305 Lightspeed Kablosuz Oyuncu Mouse",
            "price": 1299.90,
        },
        {
            "store": "Teknosa",
            "title": "Logitech G305 Lightspeed Wireless Mouse Siyah",
            "price": 1349.00,
        },
        {
            "store": "MediaMarkt",
            "title": "Logitech G305 Kablosuz Gaming Mouse",
            "price": 1249.00,
        },
        {
            "store": "Amazon TR",
            "title": "Razer DeathAdder Essential Gaming Mouse",
            "price": 899.90,
        }
    ]

    products = []
    for item in raw_products:
        item_with_url = {
            **item,
            "url": build_search_url(item["store"], item["title"])
        }
        products.append(item_with_url)

    return [p for p in products if query in p["title"].lower()]