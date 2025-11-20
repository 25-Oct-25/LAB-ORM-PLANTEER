from django.db import models

class Plant(models.Model):

    class Category(models.TextChoices):
        TREE = "tree", "Tree"
        SHRUB = "shrub", "Shrub"
        FLOWER = "flower", "Flower"
        HERB = "herb", "Herb"
        CACTUS = "cactus", "Cactus"
        OTHER = "other", "Other"

    name = models.CharField(max_length=255)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plant_images/")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

