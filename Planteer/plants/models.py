from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to="flags/", null=True, blank=True)

    def __str__(self):
        return self.name

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
    used_for = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="plant_images/", blank=True, null=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(Country, related_name="plants", blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.plant.name}'
    
   
   
