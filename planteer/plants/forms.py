from django import forms
from .models import Plant, Country, Comment

class PlantForm(forms.ModelForm):
    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Countries",
    )

    class Meta:
        model = Plant
        fields = ['name', 'about', 'category', 'is_edible', 'image', 'used_for', 'countries']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'used_for': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_edible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Write your comment...'
            }),
        }
