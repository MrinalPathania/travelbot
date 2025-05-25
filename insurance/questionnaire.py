
def run_insurance_questionnaire(destination, duration_days, nationality="Unknown"):
    print("\n🩺 Let’s run through a few quick questions to help match your travel needs with the best insurance coverage.")
    irs = 0
    reasons = []

    # SECTION 1: Health Basics
    print("\n👤 Section 1: Health Basics")

    age = int(input("1️⃣ What is your age? ").strip())
    if age > 65:
        irs += 5
        reasons.append("Age over 65")

    if input("2️⃣ Do you have high blood pressure? (yes/no): ").lower().startswith("y"):
        irs += 5
        reasons.append("High blood pressure")

    if input("3️⃣ Do you have diabetes? (yes/no): ").lower().startswith("y"):
        dtype = input("  ↳ Type 1 or Type 2?: ").strip()
        if input("  ↳ Do you use insulin? (yes/no): ").lower().startswith("y"):
            irs += 3
            reasons.append("Insulin usage")
        irs += 5
        reasons.append(f"Diabetes ({dtype})")

    if input("4️⃣ Do you have a heart condition? (yes/no): ").lower().startswith("y"):
        irs += 7
        reasons.append("Heart condition")

    if input("5️⃣ Do you currently have or recently had cancer? (yes/no): ").lower().startswith("y"):
        irs += 7
        reasons.append("Cancer")

    if input("6️⃣ Do you have kidney or liver disease? (yes/no): ").lower().startswith("y"):
        irs += 5
        reasons.append("Kidney/liver disease")

    if input("7️⃣ Do you have a terminal illness? (yes/no): ").lower().startswith("y"):
        irs += 10
        reasons.append("Terminal illness")

    # SECTION 2: Stability & Meds
    print("\n🧾 Section 2: Condition Stability (Last 90 Days)")

    if input("8️⃣ Have you been admitted to a hospital in the last 90 days? (yes/no): ").lower().startswith("y"):
        irs += 5
        reasons.append("Recent hospitalization")

    if input("9️⃣ Has your medication changed in the last 90 days? (yes/no): ").lower().startswith("y"):
        irs += 3
        reasons.append("Recent medication change")

    if input("🔟 Are you currently taking prescription medication? (yes/no): ").lower().startswith("y"):
        irs += 2
        reasons.append("On medication")

    # SECTION 3: Trip Style
    print("\n🌍 Section 3: Trip Details")

    print("What type of trip is this?")
    print("1. Leisure/Tourist\n2. Business\n3. Cruise\n4. Hiking/Camping\n5. Adventure (scuba, skiing)\n6. Extreme (mountain, jungle, Arctic)")
    trip_type = input("Select 1-6: ").strip()
    trip_scores = {"1": 0, "2": 5, "3": 5, "4": 10, "5": 15, "6": 20}
    trip_score = trip_scores.get(trip_type, 0)
    irs += trip_score
    if trip_score > 0:
        reasons.append("Trip type risk")

    # SECTION 4: Destination Risk
    print("\n🛰️ Checking destination for conflicts or advisories...")
    from utils.alerts import get_conflict_and_health_alerts
    alerts = get_conflict_and_health_alerts(destination)
    conflict_detected = any("avoid" in a.lower() or "conflict" in a.lower() for a in alerts)

    if conflict_detected:
        irs += 25
        reasons.append("Conflict zone or high-risk advisory")
        print(f"⚠️ Conflict or advisory detected for {destination}")
    else:
        print(f"✅ No major conflict or advisory detected for {destination}.")

    # SECTION 5: Duration
    if duration_days > 180:
        irs += 20
        reasons.append("Duration > 180 days")
    elif duration_days > 90:
        irs += 15
        reasons.append("Duration > 90 days")
    elif duration_days > 60:
        irs += 10
        reasons.append("Duration > 60 days")
    elif duration_days > 30:
        irs += 5
        reasons.append("Duration > 30 days")

    # SECTION 6: Optional Safety Questions
    print("\n🔒 Section 6: Optional Safety Questions (You can skip if unsure)")

    if input("Are you currently pregnant? (yes/no/skip): ").lower().startswith("y"):
        irs += 5
        reasons.append("Pregnancy")

    if input("Have you been diagnosed with anxiety, depression, or any psychiatric condition? (yes/no/skip): ").lower().startswith("y"):
        irs += 3
        reasons.append("Mental health condition")

    if input("Have you made a travel insurance claim in the last 3 years? (yes/no/skip): ").lower().startswith("y"):
        irs += 3
        reasons.append("Past insurance claims")

    if input("Do you smoke or have a history of smoking? (yes/no/skip): ").lower().startswith("y"):
        irs += 2
        reasons.append("Smoker")

    if input("Do you use recreational drugs or consume alcohol regularly? (yes/no/skip): ").lower().startswith("y"):
        irs += 3
        reasons.append("Drug or alcohol usage")

    if input("Is this trip for medical treatment or surgery abroad? (yes/no): ").lower().startswith("y"):
        irs += 25
        reasons.append("Medical tourism (usually not covered)")

    # Result summary
    print(f"\n✅ Your total Insurance Risk Score (IRS): {irs}/100")

    if irs <= 25:
        tier = "🟢 Low Risk — Standard travel insurance likely available"
    elif irs <= 50:
        tier = "🟡 Moderate Risk — Enhanced medical coverage recommended"
    elif irs <= 75:
        tier = "🟠 High Risk — Comprehensive coverage may be required"
    else:
        tier = "🔴 Very High Risk — Limited insurance availability"

    print(f"📊 Risk Tier: {tier}")

    if irs > 75:
        print("\n🚨 TRAVEL RISK NOTICE")
        print("We found flight options for your trip. However, your current risk profile suggests that travel insurance coverage may be limited or unavailable due to:")
        for r in reasons:
            print(f"• {r}")
        print("\n🚨 **We strongly recommend verifying your insurance options before booking your flight.**")

    return irs, tier