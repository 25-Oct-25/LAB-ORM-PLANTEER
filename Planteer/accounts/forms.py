from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First name")
    last_name = forms.CharField(max_length=30, required=True, label="Last name")
    username = forms.CharField(max_length=150, required=True, label="Username")
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")

    def clean_password1(self):
        pw = self.cleaned_data.get("password1")
        if pw:
            password_validation.validate_password(pw, self.instance)
        return pw
