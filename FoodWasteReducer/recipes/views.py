from django.http import JsonResponse
from django.shortcuts import render
from .models import SavedRecipe
from .utils import fetch_recipes_from_api ,generate_proper_instructions,fetch_recipe_details
import html
from bs4 import BeautifulSoup  
from django.contrib.auth.decorators import login_required



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

@login_required
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
    return render(request, 'recipes/recipe_suggestion.html', context)

@login_required
def recipe_detail(request, recipe_id):
    # For API recipes
    recipe_data = fetch_recipe_details(recipe_id)
    
    if not recipe_data:
        return render(request, '404.html', status=404)
    
    # Process ingredients into consistent format
    ingredients = []
    for ing in recipe_data.get('extendedIngredients', []):
        ingredients.append({
            'name': ing.get('name', ''),
            'amount': ing.get('amount', 0),
            'unit': ing.get('unit', '')
        })
    
    # Process instructions
    instructions = clean_html(recipe_data.get('instructions', ''))
    
    instruction_steps = [step for step in instructions.split('\n') if step.strip()]
    
    context = {
        'recipe': {
            'id': recipe_data.get('id',0),
            'title': recipe_data.get('title', ''),
            'image': recipe_data.get('image', ''),
            'readyInMinutes': recipe_data.get('readyInMinutes', 0),
            'servings': recipe_data.get('servings', 0),
            'ingredients': ingredients,
            'instructions': instructions,
            'summary': recipe_data.get('summary', ''),
            'instruction_steps': instruction_steps,
        }
    }
    return render(request, 'recipes/detailed_recipes.html', context)



@login_required
def save_recipe(request):
    if request.method == "POST":
        recipe_id = str(request.POST.get("recipe_id"))
        title = request.POST.get("title")
        image_url = request.POST.get("image_url")
        ready_in_minutes = request.POST.get("ready_in_minutes")
        servings = request.POST.get("servings")
        ingredients = request.POST.get("ingredients")
        instructions = request.POST.get("instructions")
        summary = request.POST.get("summary")

        # Check if this exact recipe is already saved by this user
        if SavedRecipe.objects.filter(
            user=request.user, 
            recipe_id=recipe_id,
            title=title,
            image_url=image_url
        ).exists():
            return JsonResponse({"status": "info", "message": "This exact recipe is already saved."})
        
        # Save the new recipe
        SavedRecipe.objects.create(
            user=request.user,
            recipe_id=recipe_id,
            title=title,
            image_url=image_url,
            ready_in_minutes=ready_in_minutes,
            servings=servings,
            ingredients=ingredients,
            instructions=instructions,
            summary=summary
        )

        return JsonResponse({"status": "success", "message": "Recipe saved successfully."})
    
    return JsonResponse({"status": "error", "message": "Invalid request."})
def about(request):
    return render(request, 'recipes/about.html')

def privacy(request):
    return render(request, 'recipes/privacy.html')
