from django.db import models


class Plant(models.Model):

    class Category(models.TextChoices):
        HOUSE = "house", "House Plant"
        OUTDOOR = "outdoor", "Outdoor"
        HERB = "herb", "Herb"
        FRUIT = "fruit", "Fruit"
        VEGETABLE = "vegetable", "Vegetable"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
