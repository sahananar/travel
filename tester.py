import requests

import os
import requests
from dotenv import load_dotenv

load_dotenv(override = True)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
print(HUGGINGFACE_API_KEY)

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

response = requests.get(API_URL, headers=headers)

print(f"🔍 DEBUG - Status Code: {response.status_code}")
print(f"🔍 DEBUG - Raw Response: {response.text}")  # Print raw response
