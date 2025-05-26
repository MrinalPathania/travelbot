
def run_visa_flow(nationality, origin_airport, destination_airport):
    print(f"🛂 Checking visa requirements via simulated Sherpa API...")
    print(f"Nationality: {nationality}")
    print(f"From: {origin_airport['country']} → To: {destination_airport['country']}")
    print("✅ Based on Sherpa simulation: No visa required for short stay.")
