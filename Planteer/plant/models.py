from django.db import models
from datetime import datetime

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=200)
    flag = models.ImageField(upload_to='plants/images/')

    def __str__(self) -> str:
        return self.name



class Plant(models.Model):
    
    class CategoryChoices(models.TextChoices):
        VEGETABLES = 'vegetables', 'Vegetables'
        FRUITS = 'fruits', 'Fruits'
        FLOWERS = 'flowers', 'Flowers'
        HERBS = 'herbs', 'Herbs'
        
    
    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/" , default='images/default.jpg')
    category = models.CharField(max_length=20, choices=CategoryChoices.choices)
    is_edible = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)
    countries = models.ManyToManyField(Country)

    def __str__(self) -> str:
        return self.name


    
class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        return self.full_name