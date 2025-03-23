import requests


API_KEY = 'fbf7e3cb11c54ddb8f3b39b750cc09c2'
BASE_URL = 'https://api.spoonacular.com/recipes/'
    

def fetch_recipe_details(recipe_id):
    """Fetch full recipe details including cooking instructions."""
    url = f"{BASE_URL}{recipe_id}/information"
    params = {'apiKey': API_KEY}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    return None

def fetch_recipes_from_api(ingredients):
    """Fetch recipes based on ingredients and get detailed info."""
    endpoint = f"{BASE_URL}findByIngredients"
    params = {
        'ingredients': ingredients,
        'number': 10,
        'apiKey': API_KEY,
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        recipes = response.json()
        
        # Fetch full details for each recipe
        detailed_recipes = []
        for recipe in recipes:
            
            details = fetch_recipe_details(recipe['id'])
            if details:
                detailed_recipes.append({
                    'title': recipe['title'],
                    'image': recipe['image'],
                    'instructions': details.get('instructions', 'Instructions not available.')
                })
        
        return detailed_recipes
    return []