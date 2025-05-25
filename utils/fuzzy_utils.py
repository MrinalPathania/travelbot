from rapidfuzz import process
from dateutil import parser
from datetime import datetime

# Month mapping
MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]

# Replace fuzzy month names before parsing
def correct_months(date_str):
    words = date_str.lower().split()
    corrected = []
    for word in words:
        match = process.extractOne(word, MONTHS, score_cutoff=60)
        corrected.append(match[0] if match else word)
    return ' '.join(corrected)

def parse_fuzzy_date(input_str):
    try:
        if not any(char.isdigit() for char in input_str if char != '/'):
            print("⚠️ You didn’t include a year. Assuming current year.")
        corrected_input = correct_months(input_str)
        return parser.parse(corrected_input, default=datetime(datetime.today().year, 1, 1))
    except Exception:
        return None


from difflib import get_close_matches

def fuzzy_yes_no(input_str):
    input_str = input_str.strip().lower()
    match = get_close_matches(input_str, ["yes", "no"], n=1, cutoff=0.5)
    return match[0] if match else input_str