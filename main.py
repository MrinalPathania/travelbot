
from insurance import run_insurance_questionnaire
from datetime import datetime

print("✈️  Welcome to Assurigo — your AI travel assistant!\n")

origin = input("Where are you flying from? (e.g., IN): ")
destination = input("Where are you flying to? (e.g., CA): ")
passport = input("What is your passport country code? (e.g., IN): ")

# --- Sherpa visa mock response ---
print("\n🛂 Checking visa requirements (mock)...")
visa_info = {
    "visa_required": True,
    "summary": "Visa is required for Indian passport holders to enter Canada.",
    "link": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada.html"
}
print("Visa Required:", visa_info["visa_required"])
print("Summary:", visa_info["summary"])
print("More info:", visa_info["link"])

# --- Collect and calculate trip length ---
print("\n🛫 Let's calculate your trip duration.")
departure = input("Enter your departure date (YYYY-MM-DD): ")
return_date = input("Enter your return date (YYYY-MM-DD): ")

try:
    dep_date = datetime.strptime(departure, "%Y-%m-%d")
    ret_date = datetime.strptime(return_date, "%Y-%m-%d")
    trip_length = (ret_date - dep_date).days
    if trip_length <= 0:
        raise ValueError("Return date must be after departure date.")
except Exception as e:
    print("⚠️ Invalid date format or logic:", e)
    exit()

print(f"🗓️ Your trip length is {trip_length} days.")

# --- Insurance scoring ---
print("\n🛡️  Let's assess your insurance needs.")
age = input("What is your age? ")
insurance_result = run_insurance_questionnaire(age, trip_length)

print("\n✅ Insurance Plan Recommendation:")
print(f"Recommended Plan: {insurance_result['plan']}")
print(f"Risk Score: {insurance_result['risk_score']}")

if insurance_result['plan'] == "Premium":
    print("Reason: Significant medical risks or trip duration flagged.")

print("\nThank you for using Assurigo!")
