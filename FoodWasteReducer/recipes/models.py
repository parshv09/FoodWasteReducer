from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField(help_text="Comma-separated list of ingredients")
    instructions = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.CharField(max_length=100)  # External API ID
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    ready_in_minutes = models.IntegerField()
    servings = models.IntegerField()
    ingredients = models.TextField()  # You can store as JSON or string
    instructions = models.TextField()
    summary = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
