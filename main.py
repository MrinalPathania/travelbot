from chatbot.dialogue_flow import handle_visa_check
# from insurance.questionnaire import run_insurance_questionnaire  # Uncomment when ready

def main():
    print("👋 Welcome to Assurigo - your AI travel assistant!")

    nationality = input("What is your nationality? (e.g., Indian): ").strip()
    destination = input("Where are you traveling to? (e.g., Canada): ").strip()

    handle_visa_check(nationality, destination)

    # After visa logic, continue to insurance
    # run_insurance_questionnaire()

    print("\n✅ Visa check complete. Next: Travel insurance logic (coming soon).")

if __name__ == "__main__":
    main()