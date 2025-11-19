from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "about", "used_for", "category", "is_edible", "image"]
