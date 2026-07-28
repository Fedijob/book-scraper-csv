import time
import requests, pandas as pd
from bs4 import BeautifulSoup

rows = []
for page in range(1, 51):  
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"skipped page {page}: {e}")
        continue

    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")

    for book in soup.select("article.product_pod"):
        rows.append({
            "title": book.h3.a["title"],
            "price": book.select_one("p.price_color").text,
            "rating": book.select_one("p.star-rating")["class"][1],
            "stock": book.select_one("p.instock").text.strip(),
        })
    time.sleep(1)
df = pd.DataFrame(rows)
df["price"] = df["price"].str.replace("£", "", regex=False).astype(float)
df["rating"] = df["rating"].map({"One":1,"Two":2,"Three":3,"Four":4,"Five":5})
df.to_csv("books.csv", index=False)
print(df.head(), len(df))