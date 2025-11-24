from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    flag = models.ImageField(upload_to='countries/flags/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



class Plant(models.Model):

    class Category(models.TextChoices):
        TREE = "tree", "Tree"
        FLOWER = "flower", "Flower"
        VEGETABLE = "vegetable", "Vegetable"
        HERB = "herb", "Herb"
        OTHER = "other", "Other"

    name = models.CharField(max_length=150)
    about = models.TextField()    
    used_for = models.TextField(help_text="What is this plant used for?")

    image = models.ImageField(upload_to="plants/")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    countries = models.ManyToManyField(Country, related_name='plants', blank=True)


def __str__(self):
    return self.name


class Comment(models.Model):
    plant = models.ForeignKey(
        'Plant',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f"Comment by {self.name} on {self.plant.name}"



