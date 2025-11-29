# --- ملف accounts/forms.py (تم تصحيح المسافات البادئة) ---

from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

# --- CustomUserForm (نموذج التسجيل المخصص - بتنسيق Bootstrap) ---
class CustomUserForm(forms.ModelForm):
    # الحقول يجب أن تكون داخل الكلاس بمسافة بادئة واحدة
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'})
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password', 'autocomplete': 'new-password'}),
        required=True
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    # دالة save يجب أن تكون جزءًا من الكلاس بمسافة بادئة واحدة
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        if commit:
            user.save()
        return user

# --- ProfileUpdateForm (نموذج تعديل الملف الشخصي) ---
class ProfileUpdateForm(forms.ModelForm):
    # الحقول بمسافة بادئة واحدة
    about = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write something about yourself...'}),
        label='Bio / About',
    )
    website_link = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
        label='Website',
    )
    avatar = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Profile Picture (Avatar)',
    )
    
    class Meta:
        model = Profile
        fields = ['about', 'avatar', 'website_link']