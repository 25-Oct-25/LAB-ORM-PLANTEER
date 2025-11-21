from django import forms
from .models import Plant
from .models import Review


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'description', 'image', 'category', 'is_edible', 'is_published']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Plant name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Write description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'is_edible': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check'}),
        }



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'comment', 'rating']
        widgets = {
            'rating': forms.Select(choices=[(i,i) for i in range(1,6)])
        }
