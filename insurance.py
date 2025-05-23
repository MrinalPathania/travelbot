
def run_insurance_questionnaire(age, trip_length):
    print("\nPlease answer the following health questions with 'yes' or 'no':")

    questions = {
        "high_blood_pressure": "Do you have high blood pressure (hypertension)?",
        "diabetes": "Do you have diabetes (Type 1 or 2)?",
        "respiratory_disease": "Do you have any chronic respiratory condition (e.g., asthma, COPD)?",
        "heart_disease": "Have you ever been diagnosed with heart disease?",
        "recent_surgery": "Have you had any surgery in the last 12 months?",
        "hospitalized": "Have you been hospitalized in the past year?",
        "prescription_meds": "Are you currently taking prescription medication?",
        "cancer": "Have you had cancer (active or within the past 5 years)?",
        "kidney_disease": "Do you have chronic kidney disease or require dialysis?",
        "liver_disease": "Do you have liver disease (e.g., cirrhosis, hepatitis)?",
        "terminal_illness": "Have you been diagnosed with a terminal illness?"
    }

    scores = {
        "high_blood_pressure": 1,
        "diabetes": 1,
        "respiratory_disease": 1,
        "heart_disease": 2,
        "recent_surgery": 2,
        "hospitalized": 2,
        "prescription_meds": 1,
        "cancer": 3,
        "kidney_disease": 3,
        "liver_disease": 3,
        "terminal_illness": 3
    }

    risk_score = 0
    answers = {}

    for key, question in questions.items():
        answer = input(question + " ").strip().lower()
        if answer == 'yes':
            risk_score += scores[key]
            answers[key] = True
        else:
            answers[key] = False

    if int(age) > 65:
        risk_score += 1

    if int(trip_length) > 30:
        risk_score += 1

    if risk_score <= 2:
        plan = "Basic"
    elif risk_score <= 5:
        plan = "Standard"
    else:
        plan = "Premium"

    return {
        "risk_score": risk_score,
        "plan": plan,
        "details": answers
    }
