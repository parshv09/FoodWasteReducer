import requests
from django.core.cache import cache
from dotenv import load_dotenv
import os 

load_dotenv()

API_KEY = os.getenv('SPOONACULAR_API_KEY')
BASE_URL = 'https://api.spoonacular.com/recipes/'
    

def fetch_recipe_details(recipe_id):
    cache_key = f"recipe_{recipe_id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    """Fetch full recipe details including cooking instructions."""
    url = f"{BASE_URL}{recipe_id}/information"
    params = {'apiKey': API_KEY}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data= response.json()
        cache.set(cache_key, data, timeout=3600)  # Cache for 1 hour
        return data
    return None

def generate_proper_instructions(recipe_title):
    """Generate realistic cooking instructions based on the recipe title."""
    instructions_dict = {
        "Frittata Muffins": """
        1. Preheat the oven to 180°C (350°F) and grease a muffin tray.
        2. In a bowl, whisk eggs with milk, salt, and pepper.
        3. Chop vegetables like bell peppers, onions, and spinach.
        4. Mix the vegetables with the egg mixture and add cheese if desired.
        5. Pour the mixture into muffin cups and bake for 15-20 minutes until set.
        6. Let them cool slightly, then remove and serve warm.
        """,
        "Pancakes": """
        1. In a mixing bowl, combine flour, sugar, baking powder, and salt.
        2. In another bowl, whisk together milk, eggs, and melted butter.
        3. Pour the wet ingredients into the dry ingredients and mix until smooth.
        4. Heat a pan over medium heat and lightly grease with butter.
        5. Pour a small amount of batter into the pan and cook until bubbles form on the surface.
        6. Flip the pancake and cook the other side until golden brown.
        7. Serve warm with syrup or fruits.
        """,
        "Tomato Soup": """
        1. Heat a pot over medium heat and add butter or olive oil.
        2. Add chopped onions and garlic, sautéing until soft.
        3. Pour in chopped tomatoes and cook for 5 minutes.
        4. Add vegetable broth, salt, pepper, and herbs like basil.
        5. Simmer for 15 minutes, then blend until smooth.
        6. Serve warm with croutons or bread.
        """
    }

    # Return predefined instructions if available, otherwise give a general format
    return instructions_dict.get(recipe_title, f"""
    1. Gather all ingredients for {recipe_title}.
    2. Follow the common method of preparing {recipe_title}.
    3. Season and adjust flavors as per your taste.
    4. Cook according to standard cooking methods.
    5. Serve and enjoy your {recipe_title}!
    """)

    

def fetch_recipes_from_api(ingredients, diet=None):
    cache_key = f"search_{ingredients}_{diet}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data
    
    """Fetch recipes based on ingredients and diet preference."""
    endpoint = f"{BASE_URL}complexSearch"
    params = {
        
        'includeIngredients': ingredients,
        'number': 5,
        'apiKey': API_KEY,
        'diet': diet.lower() if diet else None,  # Add diet filter if provided
        'instructionsRequired': True,
    }
    
    # Remove None values to avoid sending empty params
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        recipes = response.json().get('results',[])
        
        detailed_recipes = []
        for recipe in recipes:
            details = fetch_recipe_details(recipe['id'])
            if details:
                detailed_recipes.append({
                    'id': recipe['id'],
                    'title': recipe['title'],
                    'image': recipe['image'],
                    'instructions': details.get('instructions', 'Instructions not available.'),
                    'diet': diet  # Optional: Store diet info in the response
                })
        cache.set(cache_key, detailed_recipes, timeout=3600)
        return detailed_recipes
    return []