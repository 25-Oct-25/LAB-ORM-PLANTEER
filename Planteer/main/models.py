from django.db import models

# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=2048)
    last_name = models.CharField(max_length=2048)
    email = models.EmailField()
    meassage = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)