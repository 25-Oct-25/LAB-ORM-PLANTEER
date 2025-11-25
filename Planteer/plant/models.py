from django.db import models

# Create your models here.

class Country(models.Model):

    name = models.CharField(max_length=255)
    flag = models.ImageField(upload_to="flags/")

    def __str__(self) -> str:
        return self.name


class Plant(models.Model):

    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/", default="images/default.jpg")
    category = models.CharField(max_length=100)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(Country)

    def __str__(self) -> str:
        return self.name
    
    
class Review(models.Model):

    plant=models.ForeignKey(Plant, on_delete=models.CASCADE)
    name= models.CharField(max_length=1024)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.plant.name + " - " + self.name
