from django import forms
from .models import Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = '__all__'
        widgets = {
            'countries': forms.CheckboxSelectMultiple()
        }


# بس للتعليم ما استخدمتها 