import folium
from geopy.geocoders import Nominatim
import requests
import streamlit as st
from streamlit_folium import folium_static
import os
from dotenv import load_dotenv

load_dotenv()

geolocator = Nominatim(user_agent="travel_recommender")

def get_location_coordinates(place):
    try:
        location = geolocator.geocode(place, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Geolocation failed for {place}")
    except Exception as e:
        print(f"⚠️ Error getting coordinates for {place}: {e}")
    return None, None

def get_place_image(query):
    
    #UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_KEY")
    UNSPLASH_ACCESS_KEY = st.secrets["UNSPLASH_KEY"]

    if not UNSPLASH_ACCESS_KEY:
        print("Error: Unsplash API key is missing.")
        return None

    url = f"https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": UNSPLASH_ACCESS_KEY,
        "per_page": 1,
        "orientation": "landscape"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                return results[0]["urls"]["regular"]
        else:
            print(f"Unsplash API error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Could not fetch image for {query}: {e}")

    return None

def create_map(recommended_places):

    if not recommended_places:
        return folium.Map(location=[20, 0], zoom_start=2)

    first_coords = get_location_coordinates(recommended_places[0])
    map_center = first_coords if first_coords[0] is not None else [20, 0]
    
    travel_map = folium.Map(location=map_center, zoom_start=4)

    for place in recommended_places:
        lat, lon = get_location_coordinates(place)
        if lat is not None and lon is not None:
            image_url = get_place_image(place)

            popup_html = f"<b>{place}</b><br>"
            if image_url:
                popup_html += f'<img src="{image_url}" width="200px" style="border-radius:8px;">'

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"Click for details about {place}",
            ).add_to(travel_map)

    return travel_map