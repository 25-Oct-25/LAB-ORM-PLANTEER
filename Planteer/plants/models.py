from django.db import models
from django.utils import timezone
# Create your models here.

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

    def __str__(self):
        return self.name

class Comment(models.Model):
    plant = models.ForeignKey(
        Plant, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    full_name = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.full_name} on {self.plant.name}"