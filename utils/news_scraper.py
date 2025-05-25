import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime, timedelta
import os

CACHE_FILE = "news_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def search_travel_risk_news(country):
    cache = load_cache()
    today = datetime.now()
    if country in cache:
        cached = cache[country]
        if datetime.fromisoformat(cached["fetched"]) > today - timedelta(days=30):
            return cached["articles"]

    query = f"conflict OR outbreak OR epidemic OR pandemic OR travel warning site:news.google.com {country}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.bing.com/search?q={requests.utils.quote(query)}"
    articles = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print("⚠️ Failed to fetch news results.")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        for item in soup.find_all("li", class_="b_algo"):
            title_tag = item.find("h2")
            snippet = item.find("p")
            if title_tag and snippet:
                title = title_tag.get_text()
                link = title_tag.find("a")["href"]
                text = snippet.get_text()
                if any(term in text.lower() for term in ["conflict", "epidemic", "pandemic", "outbreak", "war", "warning"]):
                    articles.append({"title": title, "link": link, "snippet": text})

        cache[country] = {
            "fetched": today.isoformat(),
            "articles": articles
        }
        save_cache(cache)
        return articles
    except Exception as e:
        print(f"⚠️ Scraper error: {e}")
        return []

def show_risk_flag_and_top_articles(country):
    print(f"🔍 Checking recent headlines for safety concerns in {country}...")
    articles = search_travel_risk_news(country)
    if not articles:
        print("✅ No recent travel risk news found.")
    else:
        print(f"🚨 Risk Detected! Recent headlines for {country}:")
        for a in articles[:3]:
            print(f"- {a['title']}\n  {a['snippet']}\n  {a['link']}\n")