def run_insurance_questionnaire():
    print("\n🩺 Let's assess your travel insurance risk.")

    risk_factors = {
        "heart condition": False,
        "high blood pressure": False,
        "cancer": False,
        "kidney disease": False,
        "diabetes": None,  # Will follow up with type
    }

    answers = {}

    for condition in risk_factors:
        if condition == "diabetes":
            has_diabetes = input("Do you have diabetes? (yes/no): ").strip().lower()
            if has_diabetes == "yes":
                diabetes_type = input("Is it Type 1 or Type 2?: ").strip()
                answers["diabetes"] = diabetes_type
            else:
                answers["diabetes"] = "no"
        else:
            response = input(f"Do you have a history of {condition}? (yes/no): ").strip().lower()
            answers[condition] = response == "yes"

    # Basic risk score
    risk_score = 0
    for condition, present in answers.items():
        if present not in [False, "no"]:
            risk_score += 1

    print(f"\n🧠 Your estimated travel insurance risk score is: {risk_score}/5")

    # Placeholder: Next step to fetch insurance options
    print("🔍 Fetching matching insurance plans from your origin or destination...")