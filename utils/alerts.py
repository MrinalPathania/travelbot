
import requests
from bs4 import BeautifulSoup

def get_conflict_and_health_alerts(destination_country):
    destination = destination_country.strip().title()
    alerts = []

    travel_url = f"https://travel.gc.ca/destinations/{destination.lower().replace(' ', '-')}"
    try:
        response = requests.get(travel_url, timeout=10)
        text = response.text.lower()

        keywords = [
            "avoid all travel", "avoid non-essential travel",
            "armed conflict", "military activity", "instability",
            "high crime", "terrorism", "disease outbreak",
            "natural disaster", "evacuation", "security risk",
            "travel ban", "airspace closed", "unsafe region"
        ]

        matches = [kw for kw in keywords if kw in text]
        if matches:
            alerts.append(f"⚠️ Travel advisory detected for {destination}: " + ", ".join(matches))
        else:
            alerts.append(f"✅ No major travel advisory found for {destination}.")
    except Exception as e:
        alerts.append("❌ Unable to check travel advisory (travel.gc.ca).")

    cdc_url = "https://wwwnc.cdc.gov/travel/notices"
    try:
        response = requests.get(cdc_url, timeout=10)
        if destination.lower() in response.text.lower():
            alerts.append("🦠 CDC Health Advisory or Outbreak notice found.")
    except Exception:
        alerts.append("❌ Unable to check CDC travel notices.")

    alerts.append("🔎 You can also check WHO.int or your embassy for latest warnings.")
    return alerts
