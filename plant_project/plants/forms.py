from django import forms
from .models import Plant
from .models import Plant, Comment  # من اجل مودل التعليقات اضفت ذا السطر هنا 


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "about", "used_for", "category", "is_edible", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["username", "text"]

