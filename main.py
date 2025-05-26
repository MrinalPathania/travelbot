
import json
from pathlib import Path

# === Internal Module Imports ===
from utils.airport_lookup import get_airports_by_city
from utils.fuzzy_input import multi_suggestion_prompt
from visa_check import run_visa_flow
from alerts import run_travel_alert_check
from insurance.questionnaire import run_insurance_questionnaire
from flight_filter import run_flight_filtering


def get_airport_selection(label):
    while True:
        city = input(f"Enter the city you're flying {label} (e.g., Bangalore): ").strip()
        airports = get_airports_by_city(city)
        if not airports:
            print(f"No airports found in {city}. Try again.")
            continue

        print(f"✈️ Airports in {city.title()}:")
        for i, airport in enumerate(airports, 1):
            print(f"{i}. {airport['name']} ({airport['iata']}) - {airport['country']}")

        selection = input("Select the airport number (or type 'retry' to enter city again, or 'idk' if you're unsure): ").strip()
        if selection.lower() == "retry":
            continue
        elif selection.lower() == "idk":
            return {"name": "Unknown", "iata": None, "country": airports[0]['country']}

        try:
            index = int(selection) - 1
            if 0 <= index < len(airports):
                return airports[index]
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Invalid input. Try again.")


def main():
    print("👋 Welcome to TravelBot - your AI travel assistant!")

    # === Load Nationality List ===
    nationality_list_path = Path(__file__).parent / 'data' / 'nationality_list.json'
    with open(nationality_list_path, 'r', encoding='utf-8') as f:
        nationality_data = json.load(f)

    # === Step 1: Get Nationality ===
    print("🌎 Please enter your nationality:")
    user_input = input("You: ").strip()
    nationality = multi_suggestion_prompt(user_input, nationality_data)
    print(f"✅ Nationality selected: {nationality}")

    # === Step 2: Get Airports ===
    origin_airport = get_airport_selection("from")
    destination_airport = get_airport_selection("to")

    print(f"📍 Origin: {origin_airport['name']} ({origin_airport['iata']})")
    print(f"📍 Destination: {destination_airport['name']} ({destination_airport['iata']})")

    # === Step 3: Visa Check ===
    run_visa_flow(nationality, origin_airport, destination_airport)

    # === Step 4: Conflict or Travel Alert Check ===
    run_travel_alert_check(destination_airport['country'])

    # === Step 5: Insurance Risk Scoring ===
    run_insurance_questionnaire(nationality, destination_airport['country'])

    # === Step 6: Filter Flights Based on Transit Visa Issues or Conflict Zones ===
    run_flight_filtering(nationality, origin_airport, destination_airport)


if __name__ == "__main__":
    main()
