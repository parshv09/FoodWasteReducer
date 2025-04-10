from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('dashboard', views.inventory_dashboard, name='dashboard'),
    path('add/', views.add_food_item, name='add_food'),
]