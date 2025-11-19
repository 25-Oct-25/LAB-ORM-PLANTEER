from django.db import models

# Create your models here.

class Plant(models.Model):
    CATEGORY_CHOICES = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('succulent', 'Succulent'),
        ('herb', 'Herb'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_edible = models.BooleanField(default=False)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    native_to = models.CharField(max_length=150, blank=True, null=True)
    used_for = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name