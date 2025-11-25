


from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('flower', 'Flower'),
    ('herb', 'Herb'),
    ('vegetable', 'Vegetable'),
    ('fruit', 'Fruit'),
]


class Plant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='plants/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    countries = models.ManyToManyField("Country", related_name="plants")


    def __str__(self):
        return self.name





class Review(models.Model):
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ربط المراجعة بالمستخدم
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField()  # من 1 إلى 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plant.name}"



# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to='flags/')

    def __str__(self):
        return self.name