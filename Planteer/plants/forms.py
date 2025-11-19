from django import forms
from plants.models import Plant

class PlantForm(forms.ModelForm):
    category = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Start typing...',
            'list': 'categoryList'
        })
    )
    
    class Meta:
        model = Plant
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'used_for': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_edible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }