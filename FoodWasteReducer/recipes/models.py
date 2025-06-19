from django.db import models
from django.conf import settings



class SavedRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe_id = models.CharField(max_length=100, blank=False, null=False)  # from API
    title = models.CharField(max_length=255)
    image_url = models.URLField()
    ready_in_minutes = models.IntegerField()
    servings = models.IntegerField()
    ingredients = models.TextField()
    instructions = models.TextField()
    summary = models.TextField(blank=True)
    


    def __str__(self):
        return f"{self.title} - {self.user.username}"
