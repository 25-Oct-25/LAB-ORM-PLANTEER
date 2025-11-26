from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth.forms import UserCreationForm 
from django import forms 
from django.contrib.auth import get_user_model

User = get_user_model() 

class CustomSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') + UserCreationForm.Meta.fields
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
        return user


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('main:home_view') 
    else:
        form = CustomSignUpForm()
        
    return render(request, 'accounts/signup.html', {'form': form})