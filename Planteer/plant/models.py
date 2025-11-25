from django.db import models

# Create your models here.
class Country(models.Model):
    name =models.CharField(max_length=2048)
    image =models.ImageField(upload_to="images/", default="images/flags.png")
    
    def __str__(self):
        return self.name

class Plant(models.Model):
    class CategoryChoices(models.TextChoices):
        cat="flowering", "Flowering"
        cat1="succulents", "Succulents"
        cat2="trees", "Trees"

    name =models.CharField(max_length=2048)
    about= models.TextField()
    used_for= models.TextField()
    image =models.ImageField(upload_to="images/", default="images/default.png")
    category =models.CharField(max_length=50,choices=CategoryChoices.choices, default=CategoryChoices.cat)
    is_edible = models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    countries= models.ManyToManyField(Country)

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name =models.CharField(max_length=2048)
    last_name =models.CharField(max_length=2048)
    email =models.EmailField()
    message= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    plant=models.ForeignKey(Plant, on_delete=models.CASCADE)
    name=models.CharField(max_length=1024)
    comment= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} on {self.plant.name}"