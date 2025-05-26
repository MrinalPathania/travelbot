
from dateutil import parser
import re
from difflib import get_close_matches

MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]

def fuzzy_month_fix(text):
    words = text.lower().split()
    fixed_words = []
    for word in words:
        if word.isalpha() and word not in MONTHS:
            match = get_close_matches(word, MONTHS, n=1, cutoff=0.75)
            if match:
                fixed_words.append(match[0])
            else:
                fixed_words.append(word)
        else:
            fixed_words.append(word)
    return " ".join(fixed_words)

def run_insurance_questionnaire(nationality, destination_country):
    print(f"🩺 Let’s run through a few quick questions for travel from {nationality} to {destination_country}.")

    # Trip info
    trip_type = input("Is this a round trip or one-way? ").strip().lower()
    while trip_type not in ["round", "round trip", "one-way", "one way", "oneway"]:
        trip_type = input("Please type 'round trip' or 'one-way': ").strip().lower()

    start_input = input("When does your trip start? (e.g. 12 Oct, Oct 12, or 12/10/2025): ").strip()
    start_input = fuzzy_month_fix(start_input)

    try:
        start_date = parser.parse(start_input, fuzzy=True)
    except Exception:
        print("❌ Could not understand the start date.")
        return

    if "round" in trip_type:
        return_input = input("When is your return date? (any format): ").strip()
        return_input = fuzzy_month_fix(return_input)
        try:
            return_date = parser.parse(return_input, fuzzy=True)
            if return_date < start_date:
                print("❌ Return date cannot be before start date.")
                return
        except Exception:
            print("❌ Could not understand the return date. Please check the spelling or format.")
            return
        duration_days = (return_date - start_date).days
    else:
        duration_input = input("How many days are you planning to stay? ").strip()
        try:
            duration_days = int(duration_input)
        except ValueError:
            print("❌ Please enter a valid number of days.")
            return

    print(f"🗓️ Trip duration: {duration_days} days")

    # Grouped, polite health questionnaire
    print("🩺 Now a few quick questions about your health to help us assess your insurance needs.")
    risk_score = 0
    max_score = 12

    if input("Do you have diabetes? (yes/no): ").strip().lower() in ["yes", "y"]:
        risk_score += 2
        input("Do you have Type 1 or Type 2 diabetes? ").strip()

    if input("Do you have high blood pressure? (yes/no): ").strip().lower() in ["yes", "y"]:
        risk_score += 1

    if input("Have you had any heart-related issues? (yes/no): ").strip().lower() in ["yes", "y"]:
        risk_score += 2

    if input("Are you currently undergoing treatment for cancer or have a history of it? (yes/no): ").strip().lower() in ["yes", "y"]:
        risk_score += 3

    if input("Do you have any kidney-related conditions? (yes/no): ").strip().lower() in ["yes", "y"]:
        risk_score += 2

    if input("Are you above 60 years of age? (yes/no): ").strip().lower() in ["yes", "y"]:
        risk_score += 2

    print(f"✅ Your total travel insurance risk score is: {risk_score}/{max_score}")

    if risk_score >= 9:
        print("📊 Recommended Plan Tier: 🔴 High Risk — Comprehensive Coverage Strongly Advised")
    elif risk_score >= 5:
        print("📊 Recommended Plan Tier: 🟠 Moderate Risk — Enhanced Medical + Trip Cancellation")
    else:
        print("📊 Recommended Plan Tier: 🟢 Low Risk — Standard Plans Sufficient")
