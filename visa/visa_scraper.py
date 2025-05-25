
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

fallback_links = {
    ("Canada", "tourist"): [
        "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html"
    ],
    ("United States", "tourist"): [
        "https://travel.state.gov/content/travel/en/us-visas/tourism-visit.html"
    ],
    ("United Kingdom", "business"): [
        "https://www.gov.uk/business-visa"
    ],
}

def scrape_visa_application_links(destination, visa_type):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = f"{destination} {visa_type} visa site:gov OR site:gc.ca OR site:.gov OR site:.org"
    url = f"https://www.google.com/search?q={quote(query)}"

    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for g in soup.find_all('a'):
            href = g.get('href')
            if href and "http" in href and "url?q=" in href:
                real_link = href.split("url?q=")[-1].split("&")[0]
                if "visa" in real_link and destination.lower() in real_link.lower():
                    links.append(real_link)
            if len(links) >= 3:
                break

        if not links:
            links = fallback_links.get((destination, visa_type), [])

    except Exception:
        links = fallback_links.get((destination, visa_type), [])

    eta_mapping = {
        "Canada": 20,
        "United States": 30,
        "United Kingdom": 15,
        "Australia": 25,
    }
    avg_days = eta_mapping.get(destination, 21)

    return links, avg_days
