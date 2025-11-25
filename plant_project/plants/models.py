from django.db import models
from django.contrib.auth.models import User   # ← إضافة ضرورية


# Country Model
class Country(models.Model):
    name = models.CharField(max_length=50)
    flag = models.ImageField(upload_to="countries_flags/", blank=True, null=True)

    def __str__(self):
        return self.name


# Plant Model
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

    countries = models.ManyToManyField(
        Country,
        related_name="plants",
        blank=True
    )

    def __str__(self):
        return self.name


# Comment Model --- بعد التعديل
class Comment(models.Model):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(       # ← هنا ربطنا كل تعليق بمستخدم مسجل
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"
