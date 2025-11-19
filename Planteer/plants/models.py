from django.db import models
from django.utils import timezone

    

class Plant(models.Model):

    class CategoryChoices(models.TextChoices):
        MEDICINAL = "MED", "Medicinal"
        ORNAMENTAL = "ORN", "Ornamental"
        AROMATIC = "ARO", "Aromatic"
        FRUIT = "FRT", "Fruit Plants"
        TOXIC = "TOX", "Toxic Plants"
        INDOOR = "IN", "Indoor Plants"
        OUTDOOR = "OUT", "Outdoor Plants"

    name = models.CharField(max_length=200)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to='plants/images/', default='images/default.jpg')
    category=models.CharField(max_length=150, choices=CategoryChoices.choices)
    is_edible= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


