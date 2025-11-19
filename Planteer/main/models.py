from django.db import models
from django.utils import timezone

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField() 
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-sent_at']

    def __str__(self):
        return f"Message from: {self.first_name} {self.last_name} on: {self.sent_at.strftime('%Y-%m-%d')}"
