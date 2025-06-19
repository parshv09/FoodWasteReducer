from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from recipes.models import SavedRecipe
from inventory.models import FoodItems
from django.utils import timezone
from datetime import timedelta
from .forms import UserUpdateForm 
import requests
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
import os
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
    
    food_items_count=FoodItems.objects.filter(user=request.user)
    
    today = timezone.now().date()
    next_week = today + timedelta(days=4)

    expiring_soon_items = FoodItems.objects.filter(
        user=request.user,
        expiry_date__range=(today, next_week)
    ).order_by('expiry_date')
    return render(request, 'navigation.html', {
        'expiring_soon_items': expiring_soon_items,
        'expiring_soon_count': expiring_soon_items.count(),
        "total_recipes":saved_recipes.count(),
        "food_items_count":food_items_count.count(),
    })
    
    

load_dotenv()
User = get_user_model()                 
# ──────────────────────────────────────────────────────────────────────────────
#  HELPER – send OTP via 2Factor
# ──────────────────────────────────────────────────────────────────────────────
def _send_otp(mobile):
    api = os.getenv('TWOFACTOR_API_KEY')     # add this in settings.py or .env
    url = f"https://2factor.in/API/V1/{api}/SMS/{mobile}/AUTOGEN"
    return requests.get(url, timeout=10).json()

# ──────────────────────────────────────────────────────────────────────────────
#  HELPER – verify OTP via 2Factor
# ──────────────────────────────────────────────────────────────────────────────
def _verify_otp(session_id, otp):
    api = os.getenv('TWOFACTOR_API_KEY')
    url = f"https://2factor.in/API/V1/{api}/SMS/VERIFY/{session_id}/{otp}"
    return requests.get(url, timeout=10).json()

# ──────────────────────────────────────────────────────────────────────────────
#  MAIN VIEW  – forgot‑password  (handles all 3 steps)
# ──────────────────────────────────────────────────────────────────────────────
def forgot_password(request):
    """
    Step 1: user submits mobile  → send OTP
    Step 2: user submits OTP     → verify
    Step 3: user sets password   → save & redirect to login
    """
    # default step = 1
    step = int(request.POST.get("step", 1))

    # ── STEP 1: send OTP ────────────────────────────────────────────────────
    if request.method == "POST" and step == 1:
        mobile = request.POST.get("mobile")
        try:
            User.objects.get(mobile_number=mobile)
        except User.DoesNotExist:
            messages.error(request, "Mobile number not registered.")
        else:
            resp = _send_otp(mobile)
            if resp.get("Status") == "Success":
                request.session["fp_mobile"] = mobile
                request.session["fp_session_id"] = resp["Details"]
                step = 2
                messages.success(request, "OTP sent to your mobile.")
            else:
                messages.error(request, "Could not send OTP. Please try again.")

    # ── STEP 2: verify OTP ──────────────────────────────────────────────────
    elif request.method == "POST" and step == 2:
        otp        = request.POST.get("otp")
        mobile     = request.session.get("fp_mobile")
        session_id = request.session.get("fp_session_id")

        resp = _verify_otp(session_id, otp)
        if resp.get("Status") == "Success":
            step = 3
            messages.success(request, "OTP verified. Please set a new password.")
        else:
            messages.error(request, "Invalid OTP. Try again.")

    # ── STEP 3: set new password ────────────────────────────────────────────
    elif request.method == "POST" and step == 3:
        pw1 = request.POST.get("password")
        pw2 = request.POST.get("confirm_password")

        if pw1 != pw2:
            messages.error(request, "Passwords do not match.")
        else:
            mobile = request.session.get("fp_mobile")
            try:
                user = User.objects.get(mobile_number=mobile)
                user.set_password(pw1)
                user.save()

                # clean up session values
                for key in ("fp_mobile", "fp_session_id"):
                    request.session.pop(key, None)

                messages.success(request, "Password reset successful. Please log in.")
                return redirect("login")
            except User.DoesNotExist:
                messages.error(request, "Unexpected error. Start again.")
                step = 1

    # ── RENDER the template with current step number ────────────────────────
    return render(request, "forgot_password.html", {"step": step})

def privacy_policy(request):
    return render(request, 'privacy.html')




def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        mobile=request.POST['mobile']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        user = CustomUser.objects.create_user(username=username, email=email, mobile_number=mobile, password=password)
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



@login_required
def update_profile(request):
    if request.method=='POST':
        form=UserUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form=UserUpdateForm(instance=request.user)
    return render(request,'update_profile.html',{'form':form})

def done(request):
    return render(request, 'done.html')

def food_details(request):
    return render(request, 'food_details.html')

