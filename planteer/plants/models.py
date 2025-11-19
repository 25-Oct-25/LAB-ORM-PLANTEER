from django.db import models

# Create your models here.


class Plant(models.Model):

    class Category(models.TextChoices):
        TREE = "tree", "Tree"
        FLOWER = "flower", "Flower"
        VEGETABLE = "vegetable", "Vegetable"
        HERB = "herb", "Herb"
        OTHER = "other", "Other"

    name = models.CharField(max_length=150)
    about = models.TextField()
    native_to = models.CharField(
        max_length=150,
        blank=True,
        help_text="Country or region where this plant is native to."
    )
    used_for = models.TextField(help_text="What is this plant used for?")
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
