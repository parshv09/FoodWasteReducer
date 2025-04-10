from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'), 
    path('privacy/', views.privacy, name='privacy'),
    path('', views.recipe_suggestion, name='recipe_suggestion'),
  
]