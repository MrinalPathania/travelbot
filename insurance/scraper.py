import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def scrape_insurance_options(destination, risk_score):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_query = f"travel insurance {destination} site:.com OR site:.ca"
    url = f"https://www.google.com/search?q={quote(search_query)}"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for a in soup.find_all("a"):
            href = a.get("href")
            if href and "url?q=" in href:
                real_url = href.split("url?q=")[1].split("&")[0]
                if "insurance" in real_url and destination.lower() in real_url.lower():
                    links.append(real_url)
            if len(links) >= 5:
                break

        if not links:
            links = ["https://www.allianz-assistance.ca/en_CA.html",
                     "https://www.manulife.ca/personal/insurance/travel.html",
                     "https://www.travelsurance.ca/"]

    except Exception as e:
        links = ["https://www.allianz-assistance.ca/en_CA.html",
                 "https://www.manulife.ca/personal/insurance/travel.html",
                 "https://www.travelsurance.ca/"]

    # Mock estimated coverage tier based on risk score
    if risk_score <= 1:
        tier = "Low Risk — Standard Plans"
    elif risk_score <= 3:
        tier = "Moderate Risk — Enhanced Plans Recommended"
    else:
        tier = "High Risk — Comprehensive Plans Suggested"

    return links, tier