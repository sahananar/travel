import streamlit as st
from src.recommendation_llm import generate_recommendations_llama, extract_recommendations, extract_place_names
from src.map_utils import create_map, get_place_image
from streamlit_folium import folium_static
import re

st.header("Welcome to the TravelBot! I'm here to help you find your next travel destination 🌍")
st.write("Tell me where you've been and where you want to go, and I'll give you the top 5 places you could travel to next!")

past_travel = st.text_input("Enter a list of places you have enjoyed traveling to (separated by commas)", "")
travel_preferences = st.text_area("Enter a place you are interested in visiting:")

if st.button("Get Travel Recommendations"):
    if past_travel and travel_preferences:
        with st.spinner("Finding the best places for you..."):
            recommendations = extract_recommendations(generate_recommendations_llama(past_travel, travel_preferences))
            recommended_places = extract_place_names(recommendations)
            print(recommended_places)

            st.subheader("Here are 5 places I think you'll love to visit next!")
            st.write(recommendations)

            if recommended_places:
                st.subheader("Here is a map of these recommended places. Click on each location to see cool pictures!")
                travel_map = create_map(recommended_places)
                folium_static(travel_map)
            else:
                st.warning("⚠️ No locations found in the AI response.")
    else:
        st.warning("Please enter both past travels and preferences.")