from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Import BeautifulSoup to clean HTML


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

@login_required  # Prevents access without login
def navigation(request):
    return render(request, 'navigation.html')

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

def done(request):
    return render(request, 'done.html')

def food_details(request):
    return render(request, 'food_details.html')
