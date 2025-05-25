import pandas as pd
import re
import json

# Load your airports.csv (must be in the same folder)
airports = pd.read_csv("airports.csv")
airports = airports[airports['iata'].notna() & (airports['iata'] != '')]
airports['city'] = airports['city'].fillna('').str.strip()
airports['name'] = airports['name'].fillna('').str.strip()

# Normalize helper
def normalize(text):
    return re.sub(r'[^a-z ]', '', text.lower()).strip()

# Extract alias variants from city and airport names
def alias_variants(text):
    norm = normalize(text)
    base = re.sub(r'^(new|old|city of|saint|st) ', '', norm)
    return list(set([norm, base]))

# Build alias -> cities map
alias_map = {}
for _, row in airports.iterrows():
    aliases = alias_variants(row['city']) + alias_variants(row['name'])
    for alias in aliases:
        if alias not in alias_map:
            alias_map[alias] = set()
        alias_map[alias].add(row['city'])

# Output files
with open("utils/city_alias_map.json", "w") as f:
    json.dump({k: list(v) for k, v in alias_map.items()}, f, indent=2)

with open("utils/alias_lookup.txt", "w") as f:
    for alias in alias_map.keys():
        f.write(alias + "\n")

print("✅ Alias map and lookup list generated.")