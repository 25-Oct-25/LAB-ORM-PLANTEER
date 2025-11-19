from django.db import models
from datetime import datetime

# Create your models here.

class Plant(models.Model):
    
    class CategoryChoices(models.TextChoices):
        VEGETABLES = 'vegetables'
        FRUITS = 'fruits'
        FLOWERS = 'flowers'
        
    
    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/" , default='images/default.jpg')
    category = models.CharField(max_length=20, choices=CategoryChoices.choices)
    is_edible = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)