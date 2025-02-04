import folium
from streamlit_folium import folium_static
from map_utils import create_map, get_location_coordinates, get_place_image
import streamlit as st

# Define test places
test_places = ["Crete, Greece", "Santorini, Greece", "Athens, Greece", "Mykonos, Greece"]

# Test Geolocation Function
print("\n🔍 Testing Geolocation:")
for place in test_places:
    lat, lon = get_location_coordinates(place)
    print(f"{place} → Latitude: {lat}, Longitude: {lon}")

#Test Image Fetching
print("\nTesting Image Fetching:")
for place in test_places:
    img_url = get_place_image(place)
    print(f"{place} → Image URL: {img_url}")

# Test Map Generation
print("\nGenerating Map with Test Locations...")
travel_map = create_map(test_places)

# Save the map to an HTML file to view manually
travel_map.save("test_map.html")
print("\nMap has been saved as test_map.html!")