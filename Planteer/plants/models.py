from django.db import models

class Plant(models.Model):
    class Category(models.TextChoices):
        TREE = 'Tree', 'Tree'
        FRUIT = 'Fruit', 'Fruit'
        VEGETABLE = 'Vegetable', 'Vegetable'
        FLOWER = 'Flower', 'Flower'

    name = models.CharField(max_length=200)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/images/")
    category = models.CharField(max_length=50, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name