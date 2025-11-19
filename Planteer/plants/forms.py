from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about', 'native_to', 'used_for', 'image', 'category', 'is_edible']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 3}),
            'used_for': forms.Textarea(attrs={'rows': 2}),
        }