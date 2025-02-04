import streamlit as st
from src.recommendation_llm import generate_recommendations_llama  # Import function from existing file

st.title("✈️ AI Travel Recommender 🌍")
st.write("Tell me where you've been and where you want to go, and I'll recommend new destinations!")

# User input
past_travel = st.text_input("Places you've traveled to (comma-separated)", "")
travel_preferences = st.text_area("Describe your ideal next destination")

if st.button("Get Recommendations"):
    if past_travel and travel_preferences:
        with st.spinner("Finding the best places for you..."):
            recommendations = generate_recommendations_llama(past_travel, travel_preferences)
            st.subheader("🌍 Recommended Destinations:")
            st.write(recommendations)
    else:
        st.warning("Please enter both past travels and preferences.")
