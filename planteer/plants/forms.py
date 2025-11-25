from django import forms
from .models import Plant, Comment

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about','category', 'is_edible', 'image',  'used_for', 'countries'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your comment...', 'class': 'form-control', 'rows': 4}),
        }
