from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'), 
    path('privacy/', views.privacy, name='privacy'),
    path('recipe_Suggestion/', views.recipe_suggestion, name='recipe_suggestion'),
    path('recipe/<str:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('save-recipe/', views.save_recipe, name='save_recipe'), 
]