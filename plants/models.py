from django.db import models

class category(models.Model): #delete this class if not needed .

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
  

class Plant(models.Model):

    class Category(models.TextChoices):
        HOUSE = "house", "House Plant"
        OUTDOOR = "outdoor", "Outdoor"
        HERB = "herb", "Herb"
        FRUIT = "fruit", "Fruit"
        VEGETABLE = "vegetable", "Vegetable"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField("Country", related_name="plants", blank=True)
    

    def __str__(self):
        return self.name
class Comment(models.Model):
  
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    name = models.CharField(max_length=100)

    content = models.TextField()

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"] 

    def __str__(self):
        return f"Comment by {self.name} on {self.plant.name}"
    



class Country(models.Model):
    name = models.CharField(max_length=80, unique=True)
    flag = models.ImageField(upload_to="flags/", blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

# plants/forms.py
from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = "__all__"   # مؤقتًا: خله ياخذ كل الحقول الموجودة فعليًا
        widgets = {
            "countries": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
