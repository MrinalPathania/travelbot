from utils.airport_lookup import get_airports_by_city
from utils.fuzzy_input import multi_suggestion_prompt
import json
from pathlib import Path

def get_airport_selection(label):
    while True:
        city = input(f"Enter the city you're flying {label} (e.g., Bangalore): ").strip()
        airports = get_airports_by_city(city)
        if not airports:
            print(f"No airports found in {city}. Try again.")
            continue

        print(f"✈️ Airports in {city.lower()}:")
        for i, airport in enumerate(airports, 1):
            print(f"{i}. {airport['name']} ({airport['iata']}) - {airport['country']}")

        selection = input("Select the airport number (or type 'retry' to enter city again, or 'idk' if you're unsure): ").strip()

        if selection.lower() == "retry":
            continue
        elif selection.lower() == "idk":
            return {"name": "Unknown Airport", "iata": "XXX", "country": "Unknown"}

        if not selection.isdigit() or not (1 <= int(selection) <= len(airports)):
            print("❌ Invalid selection.")
            continue

        return airports[int(selection) - 1]

def main():
    print("👋 Welcome to TravelBot - your AI travel assistant!")

    # Ask nationality first
    nationality_list_path = Path(__file__).parent / 'data' / 'nationality_list.json'
    with open(nationality_list_path) as f:
        nationality_list = json.load(f)

    user_input_nationality = input("What is your nationality? (e.g., Indian): ").strip()
    nationality = multi_suggestion_prompt(user_input_nationality, nationality_list, label="nationality")

    origin_airport = get_airport_selection("from")
    dest_airport = get_airport_selection("to")
    # ISO fallback before fuzzy match
    from pathlib import Path
    with open(Path("data/iso_country_map.json")) as iso_file:
        iso_to_country = json.load(iso_file)
    country_code = dest_airport['country'].upper()
    if country_code in iso_to_country:
        dest_airport['country'] = iso_to_country[country_code]
        print(f"✅ ISO resolved: {country_code} → {dest_airport['country']}")
    else:
        print(f"❌ Couldn’t resolve ISO country code: {country_code}")
        return
    # ISO fallback from data/iso_country_map.json
    with open("data/iso_country_map.json") as iso_file:
        iso_to_country = json.load(iso_file)
    country_code = dest_airport['country'].upper()
    if country_code in iso_to_country:
        dest_airport['country'] = iso_to_country[country_code]
    else:
        print("❌ Couldn’t confidently resolve destination country from code.")
        return
    # ISO Alpha-2 fallback in case fuzzy match fails
    iso_to_country = {
        'UA': 'Ukraine', 'IN': 'India', 'CA': 'Canada', 'US': 'United States',
        'GB': 'United Kingdom', 'FR': 'France', 'DE': 'Germany', 'AU': 'Australia',
        'RU': 'Russia', 'CN': 'China', 'JP': 'Japan', 'BR': 'Brazil'
    }
    country_code = dest_airport['country'].upper()
    if country_code in iso_to_country:
        dest_airport['country'] = iso_to_country[country_code]
    else:
        print("❌ Couldn’t confidently resolve destination country from code.")
        return
    # Resolve airport country code to full name using country_list.json
    with open("data/country_list.json") as f:
        country_list = json.load(f)
    matches = [c for c in country_list if dest_airport['country'].lower() in [c.lower(), c[:2].lower()]]
    if matches:
        dest_airport['country'] = matches[0]
    else:
        print("❌ Couldn’t confidently resolve destination country from code.")
        return

    trip_type = input("Is this a round trip or one way? (round/one way): ").strip().lower()
    while trip_type not in ["round", "one way"]:
        trip_type = input("Please enter 'round' or 'one way': ").strip().lower()

    from dateutil import parser
    try:
        start_date = parser.parse(input("When does your trip start? (any date format): ").strip(), fuzzy=True)
    except:
        print("❌ Could not parse the start date. Try again.")
        return

    if trip_type == "round":
        try:
            end_date = parser.parse(input("When does your trip end? (any date format): ").strip(), fuzzy=True)
        except:
            print("❌ Could not parse the end date. Try again.")
            return
        duration_days = (end_date - start_date).days
    else:
        end_date = None
        duration_days = 30

    print(f"📍 From: {origin_airport['name']} ({origin_airport['iata']}) - {origin_airport['country']}")
    print(f"📍 To: {dest_airport['name']} ({dest_airport['iata']}) - {dest_airport['country']}")
    print(f"🌐 Nationality: {nationality}")
    print("🌍 Checking visa requirement for {} citizens traveling to {}...".format(nationality, dest_airport['country']))
    visa_required = True  # ← replace with real API/scraper logic in future
    if visa_required:
        visa_status = input("✋ It looks like you may need a visa to travel to this destination. Have you already obtained a visa or ETA for this trip? (yes/no): ").strip().lower()
        if visa_status != 'yes':
            print("❗ You should apply for a visa or ETA before booking.")
            print("🔗 Visit your destination country’s embassy or visa portal for more details.")
            return
        else:
            print("✅ Great — you're good to go!")
        # Conflict and health alert check
        from utils.alerts import get_conflict_and_health_alerts
        alerts = get_conflict_and_health_alerts(dest_airport['country'])
    for alert in alerts:
        print(alert)
        # Insurance questionnaire start
    else:
        print("✅ No visa needed — you're good to go!")
    print(f"📆 Trip starts on {start_date.date()} and ends on {end_date.date() if end_date else 'N/A'}. Duration: {duration_days} days.")

if __name__ == "__main__":
    main()

    # Insurance Risk Evaluation

    try:
        from insurance.questionnaire import run_insurance_questionnaire
        irs_score, risk_tier = run_insurance_questionnaire(dest_airport['country'], duration_days, nationality)
        print(f"\n✅ Your total Insurance Risk Score (IRS) is: {irs_score}/100")
        print(f"📊 Risk Tier: {risk_tier}")
    except Exception as e:
        print("❌ Failed to calculate insurance risk score. Error:", str(e))