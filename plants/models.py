from django.db import models

# Category Choices (using TextChoices exactly like slides)
class PlantCategory(models.TextChoices):
    TREE = "Tree", "Tree"
    FLOWER = "Flower", "Flower"
    VEGETABLE = "Vegetable", "Vegetable"
    FRUIT = "Fruit", "Fruit"
    HERB = "Herb", "Herb"

# Plant Model
class Plant(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/images")
    category = models.CharField(
        max_length=50,
        choices=PlantCategory.choices
    )
    is_edible = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

