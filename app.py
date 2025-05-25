import streamlit as st
from datetime import datetime
from dateutil import parser
from chatbot.dialogue_flow import handle_visa_check
from insurance.questionnaire import run_insurance_questionnaire
from geopy.geocoders import Nominatim

# Helper to get country from city
def get_country_from_city(city_name):
    geolocator = Nominatim(user_agent="travelbot")
    try:
        locations = geolocator.geocode(city_name, exactly_one=False, addressdetails=True)
        if not locations:
            return None, f"❌ Could not find any country for '{city_name}'"
        if len(locations) == 1:
            country = locations[0].raw.get('address', {}).get('country')
            return country, None
        else:
            options = [loc.raw.get('address', {}).get('country', 'Unknown') + ": " + loc.address for loc in locations]
            choice = st.selectbox(f"Multiple matches found for '{city_name}':", options)
            for loc in locations:
                if loc.address in choice:
                    return loc.raw.get('address', {}).get('country'), None
            return None, "❌ Invalid selection."
    except Exception as e:
        return None, f"⚠️ Error detecting country: {e}"

# App UI
st.title("🌍 TravelBot - Visa & Insurance Assistant")

with st.form("travel_form"):
    nationality = st.text_input("Your nationality (e.g., Indian)")
    source_city = st.text_input("City you're flying from")
    dest_city = st.text_input("City you're flying to")
    start_date = st.text_input("Trip start date (any format)")
    end_date = st.text_input("Trip end date (any format)")
    submitted = st.form_submit_button("Check Travel Requirements")

if submitted:
    try:
        start = parser.parse(start_date, default=datetime(datetime.today().year, 1, 1))
        end = parser.parse(end_date, default=datetime(datetime.today().year, 1, 1))
        duration_days = (end - start).days
        if duration_days < 1:
            st.error("End date must be after start date.")
        else:
            source_country, error1 = get_country_from_city(source_city)
            dest_country, error2 = get_country_from_city(dest_city)

            if error1: st.warning(error1)
            if error2: st.warning(error2)

            if source_country and dest_country:
                st.success(f"Traveling from {source_country} to {dest_country} for {duration_days} days")

                with st.spinner("Checking visa requirements..."):
                    handle_visa_check(nationality, dest_country)
                with st.spinner("Evaluating insurance options..."):
                    run_insurance_questionnaire(dest_country, duration_days)
    except Exception as e:
        st.error(f"❌ Failed to parse dates or lookup cities: {e}")