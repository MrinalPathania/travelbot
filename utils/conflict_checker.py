import requests
from datetime import datetime, timedelta

ACLED_API_KEY = "1UqB0rDy9wngsyV0cAI8"
ACLED_EMAIL = "mrinpathania@gmail.com"

def is_conflict_zone(destination_country):
    base_url = "https://api.acleddata.com/acled/read/"
    recent_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
    params = {
        "country": destination_country,
        "event_date": recent_date,
        "limit": 100,
        "key": ACLED_API_KEY,
        "email": ACLED_EMAIL
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"⚠️ Could not fetch conflict data (status {response.status_code}). Using fallback.")
            return False
        data = response.json().get("data", [])
        return len(data) > 0
    except Exception as e:
        print(f"⚠️ Exception while calling ACLED API: {e}")
        return False