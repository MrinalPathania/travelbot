
from rapidfuzz import process

def multi_suggestion_prompt(user_input, options):
    suggestions = process.extract(user_input, options, limit=5)

    if suggestions:
        best_match, score, _ = suggestions[0]
        if score >= 90:
            print(f"✅ Auto-selected: {best_match}")
            return best_match
        else:
            print("🔍 Did you mean one of these nationalities?")
            for i, (match, score, _) in enumerate(suggestions, 1):
                print(f"{i}. {match}")

            while True:
                selection = input("Select the number for the correct nationality, or type it manually: ").strip()
                if selection.isdigit():
                    index = int(selection)
                    if 1 <= index <= len(suggestions):
                        return suggestions[index - 1][0]
                    else:
                        print("❌ Invalid selection. Try again.")
                else:
                    manual_suggestions = process.extract(selection, options, limit=5)
                    if manual_suggestions and manual_suggestions[0][1] >= 90:
                        return manual_suggestions[0][0]
                    print("❌ Still couldn’t match confidently. Try again.")
    else:
        print("❌ No suggestions found. Please enter manually.")
        return input("Nationality: ").strip()
