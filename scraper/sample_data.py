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

def get_sample_products(query: str):
    query = query.lower()

    all_products = [
        {
            "store": "Amazon TR",
            "title": "Logitech G305 Lightspeed Kablosuz Oyuncu Mouse",
            "price": 1299.90,
            "url": "https://example.com/amazon-g305"
        },
        {
            "store": "Teknosa",
            "title": "Logitech G305 Lightspeed Wireless Mouse Siyah",
            "price": 1349.00,
            "url": "https://example.com/teknosa-g305"
        },
        {
            "store": "MediaMarkt",
            "title": "Logitech G305 Kablosuz Gaming Mouse",
            "price": 1249.00,
            "url": "https://example.com/mediamarkt-g305"
        },
        {
            "store": "Amazon TR",
            "title": "Razer DeathAdder Essential Gaming Mouse",
            "price": 899.90,
            "url": "https://example.com/amazon-razer"
        }
    ]

    return [p for p in all_products if query in p["title"].lower()]