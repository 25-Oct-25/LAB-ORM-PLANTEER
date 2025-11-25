from django import forms
from plant.models import Plant


# Create the forms class .
class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = '__all__'