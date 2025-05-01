from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from recipes.models import SavedRecipe
from inventory.models import FoodItems
from django.utils import timezone
from datetime import timedelta

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


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

@login_required 
def navigation(request):
    saved_recipes = SavedRecipe.objects.filter(user=request.user).order_by('-id')
    today = timezone.now().date()
    next_week = today + timedelta(days=7)

    expiring_soon_items = FoodItems.objects.filter(
        user=request.user,
        expiry_date__range=(today, next_week)
    ).order_by('expiry_date')
    return render(request, 'navigation.html', {
        'expiring_soon_items': expiring_soon_items,
        "total_recipes":saved_recipes.count(),
    })

def privacy_policy(request):
    return render(request, 'privacy.html')




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


@login_required
def profile(request):
    saved_recipes = SavedRecipe.objects.filter(user=request.user).order_by('-id')
    
   
    context = {
        'saved_recipes': saved_recipes[:],
        'total_recipes': saved_recipes.count(),
        'debug': True  
    }
    return render(request, 'myapp/profile.html', context)

def done(request):
    return render(request, 'done.html')

def food_details(request):
    return render(request, 'food_details.html')

