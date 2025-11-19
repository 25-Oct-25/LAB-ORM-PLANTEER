from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about','native_to','category', 'is_edible', 'image',  'used_for'] 
