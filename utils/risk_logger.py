import os
from datetime import datetime

def log_risk_score(nationality, destination, duration_days, score, tier, answers):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/session_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Nationality: {nationality}\n")
        f.write(f"Destination: {destination}\n")
        f.write(f"Trip Duration: {duration_days} days\n")
        f.write(f"Risk Score: {score}/10\n")
        f.write(f"Tier: {tier}\n\n")
        f.write("Answers:\n")
        for k, v in answers.items():
            f.write(f"- {k}: {v}\n")

    return filename