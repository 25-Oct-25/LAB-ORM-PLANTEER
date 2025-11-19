from django.db import models

class Plant(models.Model):

    
    name = models.CharField(max_length=50)

    about = models.TextField()

    used_for = models.TextField()

    image = models.ImageField(upload_to="plants_images/")

  
    class CategoryChoices(models.TextChoices):
        TREE = "Tree", "Tree"
        FRUIT = "Fruit", "Fruit"
        VEGETABLE = "Vegetables", "Vegetables"
        FLOWER = "Flower", "Flower"
        OTHER = "Other", "Other"

    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices
    )

    
    is_edible = models.BooleanField(default=False)

    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
