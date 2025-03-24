from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField(help_text="Comma-separated list of ingredients")
    instructions = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
