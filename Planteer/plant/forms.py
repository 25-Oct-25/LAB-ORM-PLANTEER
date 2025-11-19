from django import forms
from plant.models import Plant,Contact

class PlantForm(forms.ModelForm):
    class Meta:
        model=Plant
        fields="__all__"

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields="__all__"