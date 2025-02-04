import os
import requests
#from api import fetch_travel_destinations

# Load API Key
#HUGGINGFACE_API_KEY = 

def format_destinations(destinations):
    """Format travel destinations into a readable list for the LLM."""
    if not destinations:
        return "No specific places found for this destination."

    return "\n".join([
        f"{i+1}. {place['name']} ({place['city']}) - ⭐ {place['rating']} \n   📍 {place['address']}"
        for i, place in enumerate(destinations[:5])  # Limit to top 5
    ])

def generate_recommendations_llama(past_travel, travel_preferences):
    """Generate travel recommendations using Zephyr-7B and Google Places API."""
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    # Ensure cities are processed correctly
    cities = [city.strip() for city in past_travel.split(",") if city.strip()]
    if not cities:
        return "⚠️ No valid cities detected in past travel input."

    # real_places = fetch_travel_destinations(cities)
    # places_text = format_destinations(real_places)

    prompt = f"""
    The user has previously traveled to: {', '.join(cities)}.
    They are looking for a destination that matches these preferences: {travel_preferences}.

    Given this information, suggest the best 5 destinations and explain why they match the user's interests.
    """

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_length": 500}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.json()}"

# Test the function
if __name__ == "__main__":
    past_travel = input("✈️ Enter places you've traveled to and enjoyed (comma-separated): ").strip()
    travel_preferences = input("🏝️ Describe your ideal next destination: ").strip()
    
    recommendations = generate_recommendations_llama(past_travel, travel_preferences)
    print("\n Here are some places you might like to visit next! \n")
    print(recommendations)
