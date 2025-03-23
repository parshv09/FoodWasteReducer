from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .utils import fetch_recipes_from_api 
import html
from bs4 import BeautifulSoup  # Import BeautifulSoup to clean HTML


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def inventory(request):
    return render(request, 'inventory.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = user.username  # Store username in session
            messages.success(request, "Login successful!")
            return redirect('navigation')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required  # Prevents access without login
def navigation(request):
    return render(request, 'navigation.html')

def privacy_policy(request):
    return render(request, 'privacy.html')




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

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')

def done(request):
    return render(request, 'done.html')

def food_details(request):
    return render(request, 'food_details.html')
