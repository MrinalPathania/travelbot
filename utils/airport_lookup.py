import pandas as pd
from rapidfuzz import fuzz, process
import json

AIRPORTS_FILE = "airports.csv"
ALIAS_MAP_FILE = "utils/city_alias_map.json"
ALIAS_LOOKUP_FILE = "utils/alias_lookup.txt"

# Load airport dataset
df = pd.read_csv(AIRPORTS_FILE)
df = df[df['iata'].notna() & (df['iata'] != '')]
df['city'] = df['city'].fillna('').str.strip()
df['name'] = df['name'].fillna('').str.strip()

# Load city alias data
with open(ALIAS_MAP_FILE, "r") as f:
    alias_map = json.load(f)
with open(ALIAS_LOOKUP_FILE, "r") as f:
    alias_lookup = [line.strip() for line in f.readlines()]

def get_airports_by_city(city_input):
    normalized_input = city_input.strip().lower()
    results = process.extract(normalized_input, alias_lookup, scorer=fuzz.token_sort_ratio, limit=5)
    filtered = [r for r in results if r[1] >= 50]

    if not filtered:
        print(f"❌ No close cities found for '{city_input}'. Please check your spelling or try a nearby major city.")
        return []

    print("Did you mean one of these cities?")
    for i, (match, _, _) in enumerate(filtered, start=1):
        print(f"{i}. {match.title()}")

    try:
        selection = int(input("Select the number for the correct city: ").strip())
        selected_alias = filtered[selection - 1][0]
    except:
        print("❌ Invalid selection.")
        return []

    matched_cities = alias_map.get(selected_alias, [])
    matches = df[df['city'].isin(matched_cities)]

    return [{
        "name": row["name"],
        "iata": row["iata"],
        "icao": row["icao"],
        "city": row["city"],
        "country": row["country_full_name"],
        "lat": row["lat"],
        "lon": row["lon"]
    } for _, row in matches.iterrows()]