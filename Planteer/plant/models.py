from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=50)
    flag = models.ImageField(upload_to='flags/')

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

class Plant(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to='plants/')
    

    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    native_countries = models.ManyToManyField(Country, related_name="plants")

    def __str__(self):
        return self.name

class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    full_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.plant.name}"