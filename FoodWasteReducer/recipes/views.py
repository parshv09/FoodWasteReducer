from django.shortcuts import render
from .models import Recipe
from .utils import fetch_recipes_from_api 
import html
from bs4 import BeautifulSoup  


def clean_html(raw_html):
    """Remove HTML and format instructions with step numbers."""
    if raw_html:
        # 1. Decode HTML entities (e.g., &lt;li&gt; → <li>)
        decoded_html = html.unescape(raw_html)
        
        # 2. Use BeautifulSoup to remove all HTML tags
        soup = BeautifulSoup(decoded_html, "html.parser")
        clean_text = soup.get_text(separator="\n").strip()  # Ensures readable format

        # 3. Split into steps using new lines
        steps = clean_text.split("\n")

        # 4. Add step numbers (only for non-empty lines)
        formatted_steps = [f"{i+1}. {step.strip()}" for i, step in enumerate(steps) if step.strip()]

        return "\n".join(formatted_steps)  # Join numbered steps into a string
    
    return "Instructions not available."

def recipe_suggestion(request):
    recipes_api = []
    recipes_local = []
    ingredients_query = ''

    if request.method == 'GET' and 'food-item' in request.GET:
        food_items = request.GET.getlist('food-item')
        ingredients_query = ','.join(item.strip() for item in food_items if item.strip())

        recipes_api = fetch_recipes_from_api(ingredients_query)
        recipes_local = Recipe.objects.filter(ingredients__icontains=ingredients_query)

        for recipe in recipes_api:
            raw_instructions = recipe.get("instructions", "")
            recipe["instructions"] = clean_html(raw_instructions)  # Clean it properly!

    context = {
        'ingredients': ingredients_query,
        'recipes_api': recipes_api,
        'recipes_local': recipes_local,
    }
    return render(request, 'recipe_suggestion.html', context)

def about(request):
    return render(request, 'recipes/about.html')

def privacy(request):
    return render(request, 'recipes/privacy.html')# Create your views here.
