from django import forms
from .models import Plant, Comment  


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "about", "used_for", "category", "is_edible", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]  
        widgets = {
            "text": forms.Textarea(attrs={
                "placeholder": "Write your comment...",
                "rows": 3
            })
        }
