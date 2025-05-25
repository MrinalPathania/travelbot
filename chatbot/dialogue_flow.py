from visa.visa_scraper import scrape_visa_application_links
from utils.fuzzy_utils import fuzzy_yes_no
from utils.fuzzy_input import multi_suggestion_prompt
import json
with open('utils/country_alias_map.json') as f:
    country_alias_map = json.load(f)

def normalize_country(input_country):
    key = input_country.strip().lower()
    return country_alias_map.get(key, input_country)

from utils.fuzzy_input import multi_suggestion_prompt

def handle_visa_check(nationality, destination_country):
    destination_country = normalize_country(destination_country)
    destination_country = multi_suggestion_prompt(destination_country, [
        
        "Canada", "United States", "India", "United Kingdom", "France", "Germany", "Japan", "Australia", "Brazil", "China"
    ], label="destination countries") or destination_country
    print(f"🌍 Checking visa requirement for {nationality} citizens traveling to {destination_country}...")
    needs_visa = True  # Assume visa is needed for demonstration

    if needs_visa:
        print("✋ It looks like you may need a visa to travel to this destination.")
        has_visa = fuzzy_yes_no(input("Have you already obtained a visa or ETA for this trip? (yes/no): ")).strip().lower()
        if has_visa == "yes":
            print("✅ Great — you're good to go!")
            return
        else:
            print("✋ No problem — let’s help you with that.")
            print("We can show you official visa application links and what documents you might need.")
            apply_now = fuzzy_yes_no(input("Would you like to find visa application instructions now? (yes/no): ")).strip().lower()
            if apply_now == "yes":
                print("🔍 Searching for application links...")
                links, eta_days = scrape_visa_application_links(nationality, destination_country)
                for link in links:
                    print(f"- {link}")
                print(f"📅 Visa processing time is typically around {eta_days} days. Apply early to be safe!")
            else:
                print("🕐 No worries — you can come back later when you're ready.")
    else:
        print("✅ You don’t need a visa for this trip!")

    print("✔️ Visa check complete. Moving to insurance...")