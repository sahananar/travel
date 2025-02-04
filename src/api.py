import googlemaps
import os
import requests

# Load API Key
GOOGLE_API_KEY = 'AIzaSyAG37BYDeksPRqT8XcbObxD01cH0gqkOAc'
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

GOOGLE_SEARCH_API_KEY = 'AIzaSyBYLnY8-h7BMYTYVPSaT_Dv0fg7bIAn8uQ'
SEARCH_ENGINE_ID = "9477c3a5965a14b30"

def fetch_tripadvisor_insights(place):
    """Fetch top TripAdvisor user review insights using Google Search API."""
    
    # More targeted search query for reviews
    search_query = f'"Visiting {place}" site:tripadvisor.com'

    search_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": search_query,
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "num": 5
    }

    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        search_results = response.json().get("items", [])

        # Extract relevant snippets
        insights = []
        for result in search_results:
            snippet = result.get("snippet", "No summary available")

            # Filter out irrelevant text (e.g., "See Tripadvisor's reviews")
            if "Things to Do" in snippet or "See Tripadvisor" in snippet:
                continue

            insights.append(snippet)

            # Limit to 2 good insights
            if len(insights) >= 2:
                break
        
        # If no good insights found, return a default message
        if not insights:
            return ["No detailed user reviews found."]

        return insights
    else:
        return [f"Error {response.status_code}: {response.json()}"]

if __name__ == "__main__":
    test_places = ["Sydney, Australia", "Paris, France", "Tokyo, Japan"]

    for place in test_places:
        insights = fetch_tripadvisor_insights(place)
        print(f"\n📝 TripAdvisor Insights for {place}:")
        for idx, review in enumerate(insights):
            print(f"🔹 Insight {idx+1}: {review}")
