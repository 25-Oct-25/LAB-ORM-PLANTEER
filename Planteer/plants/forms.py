from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about', 'used_for', 'image', 'category', 'is_edible']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'used_for': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_edible': forms.CheckboxInput(),
        }
