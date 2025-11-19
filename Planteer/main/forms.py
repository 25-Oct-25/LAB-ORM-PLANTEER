from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    """Form to send contact messages from the 'Contact Us' page."""
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@domain.net'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your message...'}),
        }
