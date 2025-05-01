from django.urls import path
from . import views

#app_name = 'inventory'

urlpatterns = [
    path('dashboard/', views.inventory_dashboard, name='dashboard'),
    path('add/', views.add_food, name='add_food'),
    path('use/<int:item_id>/', views.use_food_item, name='use_food_item'),
    path('edit/<int:item_id>/', views.edit_food_item, name='edit_food_item'),
    path('delete/<int:item_id>/', views.delete_food_item, name='delete_food_item'),
]