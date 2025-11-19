from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'description', 'category', 'is_edible', 'image', 'native_to', 'used_for']
