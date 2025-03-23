from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('inventory/', views.inventory, name='inventory'),
    path('login/', views.login_view, name='login'),
    path('navigation/', views.navigation, name='navigation'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('recipes/', views.recipe_suggestion, name='recipes'),
    path('register/', views.register, name='register'),
    path('done/', views.done, name='done'),
    path('food_details/', views.food_details, name='food_details'),
     path('logout/', views.logout_view, name='logout'),

]
