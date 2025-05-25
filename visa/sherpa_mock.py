
def needs_visa(nationality, destination_country):
    # Mocked logic: assume Indian passport needs visa for some countries
    visa_required_countries = ["Canada", "United States", "United Kingdom", "Australia"]
    if nationality.lower() == "indian" and destination_country in visa_required_countries:
        return True
    return False
