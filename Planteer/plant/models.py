from django.db import models

# Create your models here.

class Plant(models.Model):

    class Category(models.TextChoices):
        FRUIT = 'Fruit', 'Fruit'
        VEGETABLE = 'Vegetable', 'Vegetable'
        HERB = 'Herb', 'Herb'
        FLOWER = 'Flower', 'Flower'
    
    name = models.CharField(max_length=100)
    about = models.TextField(max_length=100)
    used_for = models.TextField(max_length=100)
    image = models.ImageField(upload_to='plants/')
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
