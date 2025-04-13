
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
    diet_type = request.GET.get('diet-type', '').strip()  # Get diet type from request

    if request.method == 'GET' and 'food-item' in request.GET:
        food_items = request.GET.getlist('food-item') or request.GET.get('food-item', '').split(',')
        ingredients_query = ', '.join(set(item.strip() for item in food_items if item.strip()))

        # Pass diet_type to the API fetcher
        recipes_api = fetch_recipes_from_api(ingredients_query, diet=diet_type if diet_type else None)
        
        # (Optional) Filter local recipes by diet type if needed
       # recipes_local = Recipe.objects.filter(ingredients__icontains=ingredients_query)
       # if diet_type:
         #   recipes_local = recipes_local.filter(diet_type__iexact=diet_type)  # Assuming your Recipe model has a `diet_type` field

        for recipe in recipes_api:
            raw_instructions = recipe.get("instructions", "")
            if raw_instructions:
                recipe["instructions"] = clean_html(raw_instructions)
            else:
                recipe["instructions"] = generate_proper_instructions(recipe.get("title", "Delicious Dish"))

    context = {
        'ingredients': ingredients_query,
        'diet_type': diet_type,  # Pass diet_type to template (optional)
        'recipes_api': recipes_api,
        'recipes_local': recipes_local,
    }
    return render(request, 'recipe_suggestion.html', context)

def about(request):
    return render(request, 'recipes/about.html')

def privacy(request):
    return render(request, 'recipes/privacy.html')
