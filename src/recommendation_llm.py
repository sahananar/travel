import os
import requests
from dotenv import load_dotenv
import re

load_dotenv(override = True)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def extract_recommendations(output):

    lines = output.split("\n")
    extracted_lines = []

    for line in lines:
        if line.strip().startswith(("1.", "2.", "3.", "4.", "5.")): 
            extracted_lines.append(line)

    if extracted_lines:
        return "\n".join(extracted_lines)
    else:
        return output

def extract_place_names(recommendations):
    
    recommended_places = []
    pattern = r'\d+\.\s*([\w\s-]+?)[\s\-:,\.]+([\w\s]+)'

    for line in recommendations.split("\n"):
        match = re.search(pattern, line)
        
        if match:
            city = match.group(1).strip()
            country = match.group(2).strip()
            recommended_places.append(f"{city}, {country}")

    return recommended_places

# def generate_recommendations_llama(past_travel, travel_preferences):
    
#     API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
#     headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

#     places = [place.strip() for place in past_travel.split(",") if place.strip()]
#     if not places:
#         return "No valid places detected in past travel input. Please try again."

#     prompt = f"""
#     The user has previously traveled to: {', '.join(places)}.
#     They are looking for a destination that matches these preferences: {travel_preferences}.

#     Given this information, suggest the best 5 destinations and explain why they match the user's interests.

#     ### Instructions:
#     - List exactly 5 destinations.
#     - Each destination should follow this strict format:  
#     `1. <City, Country>: <Brief description>`
#     - Do NOT use "Destination 1", "Option 1", or any other variation—only the numbers `1.` to `5.`.
#     - Ensure each destination is on a new line.

#     Now, generate your recommendations in this exact format:
#     """

#     payload = {"inputs": prompt, "parameters": {"temperature": 0.7, "max_length": 500}}

#     response = requests.post(API_URL, headers=headers, json=payload)

#     if response.status_code == 200:
#         return response.json()[0]["generated_text"]
#     else:
#         return f"Error: {response.json()}"

def generate_recommendations_llama(past_travel, travel_preferences):
    
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    places = [place.strip() for place in past_travel.split(",") if place.strip()]
    if not places:
        return "No valid places detected in past travel input. Please try again."

    prompt = f"""
    The user has previously traveled to: {', '.join(places)}.
    They are looking for a destination that matches these preferences: {travel_preferences}.

    Given this information, suggest the best 5 destinations and explain why they match the user's interests.

    ### Instructions:
    - List exactly 5 destinations.
    - Each destination should follow this strict format:  
    `1. <City, Country>: <Brief description>`
    - Do NOT use "Destination 1", "Option 1", or any other variation—only the numbers `1.` to `5.`.
    - Ensure each destination is on a new line.

    Now, generate your recommendations in this exact format:
    """

    payload = {"inputs": prompt, "parameters": {"temperature": 0.7, "max_length": 500}}

    # 🚨 Debugging: Print what is being sent
    print(f"🔍 DEBUG - Sending Request to: {API_URL}")
    print(f"🔍 DEBUG - Headers: {headers}")
    print(f"🔍 DEBUG - Payload: {payload}")

    response = requests.post(API_URL, headers=headers, json=payload)

    # 🚨 Debugging: Print Full Response
    print(f"🔍 DEBUG - Response Status: {response.status_code}")
    print(f"🔍 DEBUG - Response Content: {response.json()}")

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.json()}"
