import streamlit as st

# Debugging API Keys
print(f"🔍 Hugging Face API Key: {st.secrets.get('HUGGINGFACE_API_KEY')}")
print(f"🔍 Unsplash API Key: {st.secrets.get('UNSPLASH_KEY')}")
print(f"🔍 Google API Key: {st.secrets.get('GOOGLE_API_KEY')}")