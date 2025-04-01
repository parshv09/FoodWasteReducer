from django.shortcuts import render
from .models import Recipe
from .utils import fetch_recipes_from_api ,generate_proper_instructions
import html
from bs4 import BeautifulSoup  
  


def clean_html(raw_html):
    """Remove HTML and format instructions with step numbers."""
    if not raw_html:
        return "Instructions not available."

    decoded_html = html.unescape(raw_html)
    soup = BeautifulSoup(decoded_html, "html.parser")
    clean_text = soup.get_text(separator="\n").strip()

    steps = clean_text.split("\n")
    formatted_steps = [f"{i+1}. {step.strip()}" for i, step in enumerate(steps) if step.strip()]

    return "\n".join(formatted_steps)

def recipe_suggestion(request):
    recipes_api = []
    recipes_local = []
    ingredients_query = ''

    if request.method == 'GET' and 'food-item' in request.GET:
        food_items = request.GET.getlist('food-item') or request.GET.get('food-item', '').split(',')
        ingredients_query = ', '.join(set(item.strip() for item in food_items if item.strip()))

        recipes_api = fetch_recipes_from_api(ingredients_query)
        recipes_local = Recipe.objects.filter(ingredients__icontains=ingredients_query)

        for recipe in recipes_api:
            raw_instructions = recipe.get("instructions", "")

            if raw_instructions:  # ✅ If Spoonacular provides instructions
                recipe["instructions"] = clean_html(raw_instructions)
            else:  # ❌ If missing, generate proper instructions based on recipe title
                recipe_title = recipe.get("title", "Delicious Dish")
                recipe["instructions"] = generate_proper_instructions(recipe_title)  

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
