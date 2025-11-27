from django import forms
from .models import Plant, Comment

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        # UPDATED: استبدال 'native_to' بـ 'countries'
        fields = ['name', 'description', 'category', 'is_edible', 'image', 'countries', 'used_for']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Your Comment'}),
        }
