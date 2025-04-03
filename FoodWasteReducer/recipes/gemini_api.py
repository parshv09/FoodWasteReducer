import google.generativeai as genai
import os
import requests
from django.conf import settings

# Set up Google Gemini API key
GEMINI_API_KEY = "AIzaSyBY5km4GXIyuRNMNlwJIHIglZVjQkD3CuA"
genai.configure(api_key=GEMINI_API_KEY)

# Unsplash API key
UNSPLASH_API_KEY = "your_unsplash_api_key_here"
UNSPLASH_URL = "https://api.unsplash.com/photos/random"

def fetch_recipe_image(query):
    """Fetches an image from Unsplash based on the recipe query"""
    headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
    params = {"query": query, "orientation": "landscape", "count": 1}
    response = requests.get(UNSPLASH_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['urls']['regular']  # Image URL from Unsplash
    return None

def fetch_recipes_from_gemini(ingredients):
    """
    Uses Google Gemini API to generate recipe suggestions based on given ingredients.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")  # Use the best available model
        prompt = f"I have the following ingredients: {ingredients}. Suggest a recipe with step-by-step instructions."
        response = model.generate_content(prompt)

        # Extract and clean the text response
        recipe_text = response.text if response and response.text else "No recipes found. Try different ingredients."
        
        # Now fetch a related recipe image
        recipe_image = fetch_recipe_image(ingredients)

        return {
            "instructions": recipe_text,
            "image_url": recipe_image  # Add the image URL here
        }

    except Exception as e:
        return f"Error fetching recipes: {str(e)}"