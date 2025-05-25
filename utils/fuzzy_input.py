import json
from pathlib import Path

from rapidfuzz import process

country_list_path = Path(__file__).parent.parent / 'data' / 'country_list.json'
with open(country_list_path) as f:
    COUNTRY_LIST = json.load(f)

nationality_list_path = Path(__file__).parent.parent / 'data' / 'nationality_list.json'
with open(nationality_list_path) as f:
    NATIONALITY_LIST = json.load(f)

def multi_suggestion_prompt(user_input, options, label="option", max_suggestions=3):
    user_input = user_input.strip().title()

    # Check for exact match first
    if user_input in options:
        return user_input

    # Get fuzzy matches
    suggestions = process.extract(user_input, options, limit=max_suggestions)
    threshold = 70
    strong_matches = [s[0] for s in suggestions if s[1] >= threshold]

    if not strong_matches:
        print(f"❌ Couldn’t confidently match '{user_input}' to any {label}.")
        manual = input(f"Please enter the correct {label} manually (we'll still check for typos): ").strip().title()
        return multi_suggestion_prompt(manual, options, label)

    print(f"🔍 Did you mean one of these {label}s?")
    for i, match in enumerate(strong_matches, 1):
        print(f"{i}. {match}")

    selection = input(f"Select the number for the correct {label}, or type it manually: ").strip()

    if selection.isdigit():
        idx = int(selection)
        if 1 <= idx <= len(strong_matches):
            return strong_matches[idx - 1]
        else:
            print("❌ Invalid number.")
            manual = input(f"Please enter the correct {label} manually (we'll check again): ").strip().title()
            return multi_suggestion_prompt(manual, options, label)
    else:
        # Retry fuzzy match on typed value
        return multi_suggestion_prompt(selection, options, label)
