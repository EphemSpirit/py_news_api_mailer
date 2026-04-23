from dotenv import load_dotenv
import requests
import os

load_dotenv()

res = requests.get(
    os.getenv("REQUEST_URL"),
    headers={"User-Agent": "Mozilla/5.0"}
)
content = res.json()
articles = content["articles"]

for article in content["articles"]:
    print(article["title"])
