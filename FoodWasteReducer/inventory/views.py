from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FoodItem
from .forms import FoodItemForm

@login_required
def inventory_dashboard(request):
    try:
        food_items = FoodItem.objects.filter(user=request.user).order_by('expiry_date')
        expiring_soon = [item for item in food_items if item.is_expiring_soon()]
    except Exception as e:
        food_items = FoodItem.objects.none()
        expiring_soon = []
        messages.error(request, f"Error loading inventory: {str(e)}")
    
    return render(request, 'inventory/dashboard.html', {
        'food_items': food_items,
        'expiring_soon': expiring_soon
    })

@login_required
def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            try:
                food_item = form.save(commit=False)
                food_item.user = request.user
                food_item.save()
                messages.success(request, f"{food_item.name} added successfully!")
                return redirect('inventory:dashboard')
            except Exception as e:
                messages.error(request, f"Error saving item: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = FoodItemForm()
    
    return render(request, 'inventory/add_food.html', {'form': form})   