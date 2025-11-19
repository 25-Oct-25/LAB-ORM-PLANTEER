from django.db import models

# Create your models here.
class Plant(models.Model):

  class Category(models.TextChoices):
    TREE = "tree", "Tree"                       # شجرة
    SHRUB = "shrub", "Shrub"                    # شجيرة
    SUBSHRUB = "subshrub", "Subshrub"           # شجيرة صغيرة
    HERB = "herb", "Herb"                       # نبات عشبي
    GRAMINOID = "graminoid", "Graminoid"        # نباتات نجيلية (Grass/Sedge/Rush)
    VINE = "vine", "Vine"                       # متسلق
    PALM = "palm", "Palm"                       # نخيل
    CACTUS = "cactus", "Cactus"                 # صباريات
    AQUATIC_FLOATING = "aquatic_floating", "Floating Aquatic Plant"     # نبات مائي طافٍ


  name = models.CharField(max_length=100)
  about = models.TextField()
  used_for = models.TextField()
  native_to = models.CharField(max_length=200, null=True)
  image = models.ImageField(upload_to='plants/images/')
  category =models.CharField(max_length=50, choices=Category.choices)
  is_edible = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)