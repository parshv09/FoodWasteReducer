from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FoodItems
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def inventory_dashboard(request):
    try:
        today = timezone.now().date()
        query = request.GET.get('search', '')
        category_filter = request.GET.get('category', '')
        sort_by = request.GET.get('sort', 'expiry_date')  # default sort

        food_items = FoodItems.objects.filter(user=request.user)

        # Search
        if query:
            food_items = food_items.filter(name__icontains=query)

        # Category Filter
        if category_filter and category_filter != 'ALL':
            food_items = food_items.filter(category=category_filter)

        # Sorting
        if sort_by == 'name':
            food_items = food_items.order_by('name')
        elif sort_by == 'date_added':
            food_items = food_items.order_by('-added_date')
        else:  # default to expiry_date
            food_items = food_items.order_by('expiry_date')

        # Stats
        total_items = food_items.count()
        expiring_soon = [item for item in food_items if item.is_expiring_soon()]
        expired_count = food_items.filter(expiry_date__lt=today).count()
        category_count = food_items.values('category').distinct().count()

        # Pagination
        paginator = Paginator(food_items, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except Exception as e:
        messages.error(request, f"Error loading inventory: {str(e)}")
        page_obj = []
        expiring_soon = []
        total_items = expired_count = category_count = 0

    return render(request, 'inventory/dashboard.html', {
        'page_obj': page_obj,
        'today': today,
        'total_items': total_items,
        'expired_count': expired_count,
        'category_count': category_count,
        'expiring_soon': expiring_soon,
        'search_query': query,
        'selected_category': category_filter,
        'selected_sort': sort_by,
    })



@login_required
def add_food(request):
    if request.method == 'POST':
        item_count = sum(1 for key in request.POST if key.startswith('name_'))

        try:
            for i in range(item_count):
                name = request.POST.get(f'name_{i}')
                quantity = request.POST.get(f'quantity_{i}')
                category = request.POST.get(f'category_{i}')
                expiry_date = request.POST.get(f'expiry_date_{i}')

                if name and quantity and category and expiry_date:
                    FoodItems.objects.create(
                        user=request.user,
                        name=name.strip(),
                        quantity=int(quantity),
                        category=category,
                        expiry_date=expiry_date
                    )
            messages.success(request, "Food items added successfully.")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error adding food items: {str(e)}")

    return render(request, 'inventory/add_food.html', {
        'today': timezone.now().date()
    })


@login_required
def use_food_item(request, item_id):
    item = get_object_or_404(FoodItems, id=item_id, user=request.user)
    item.delete()
    messages.success(request, f"{item.name} marked as used and removed.")
    return redirect('dashboard')

@login_required
def delete_food_item(request, item_id):
    item = get_object_or_404(FoodItems, id=item_id, user=request.user)
    item.delete()
    messages.success(request, f"{item.name} deleted.")
    return redirect('dashboard')

@login_required
def edit_food_item(request, item_id):
    item = get_object_or_404(FoodItems, id=item_id, user=request.user)

    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.quantity = request.POST.get('quantity')
        item.category = request.POST.get('category')
        item.expiry_date = request.POST.get('expiry_date')
        item.save()
        messages.success(request, f"{item.name} updated successfully.")
        return redirect('dashboard')

    return render(request, 'inventory/edit_food.html', {'item': item})