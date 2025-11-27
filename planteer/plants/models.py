from django.db import models

# 1. النموذج الجديد: الدولة
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    flag = models.ImageField(upload_to='countries/flags/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Countries" 

    def __str__(self):
        return self.name

# 2. تحديث نموذج النبات (Plant)
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
    
    # UPDATED: استبدال native_to بحقل علاقة Many-to-Many مع الدول
    countries = models.ManyToManyField(
        Country,
        related_name='native_plants',
        blank=True
    )
    
    # تم إزالة الحقل النصي القديم native_to
    # native_to = models.CharField(max_length=150, blank=True, null=True) 
    
    used_for = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 3. نموذج التعليقات (Comment) - تأكدت من مكانه كنموذج منفصل
class Comment(models.Model):
    plant = models.ForeignKey(
        'Plant', 
        on_delete=models.CASCADE,
        related_name='comments'
    )

    name = models.CharField(max_length=80)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] 

    def __str__(self):
        return f'Comment by {self.name} on {self.plant.name}'