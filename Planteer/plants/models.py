from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Country Name")
    flag = models.ImageField(upload_to='countries_flags/', blank=True, null=True, verbose_name="Flag Image")

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        
    def __str__(self):
        return self.name
    
class Plant(models.Model):
    
    class CategoryChoices (models.TextChoices):
        MEDICINAL = "MED", "Medicinal "
        ORNAMENTAL = "ORN", "Ornamental "
        AROMATIC = "ARO", "Aromatic "
        FRUIT = "FRT", "Fruit Plants "
        TOXIC = "TOX", "Toxic Plants "
        INDOOR = "IN", "Indoor Plants "
        OUTDOOR = "OUT", "Outdoor Plants"
           
    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to='plants/image/', default='images/default.png')
    category=models.CharField(max_length=150, choices=CategoryChoices.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(
        Country, 
        related_name='native_plants', 
        blank=True, 
        verbose_name="Native Countries"
    )
    
    def __str__(self):
        return self.name
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    plant = models.ForeignKey(
        Plant, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    full_name = models.CharField(max_length=150) 
    email = models.EmailField(max_length=254)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username if self.user else self.full_name} on {self.plant.name}"