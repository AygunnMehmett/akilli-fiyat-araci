import requests
from bs4 import BeautifulSoup

def search_product(query):
    url = f"https://www.hepsiburada.com/ara?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=20)

    print("Status code:", r.status_code)
    print("HTML uzunluğu:", len(r.text))
    print(r.text[:1000])  # ilk 1000 karakteri göster

    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.find_all("a")
    print("Bulunan a etiketi sayısı:", len(items))

    return []

if __name__ == "__main__":
    search_product("iphone")