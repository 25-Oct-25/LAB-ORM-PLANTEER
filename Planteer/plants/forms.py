from django import forms
from .models import Plant, Comment 

class PlantForm(forms.ModelForm):
    """نموذج لإضافة وتعديل بيانات النبات (Plant)."""
    class Meta:
        model = Plant
        fields = ['name', 'about', 'used_for', 'image', 'category', 'is_edible']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم النبات'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'الوصف الكامل للنبات'}),
            'used_for': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'الاستخدامات والفوائد'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_edible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CommentForm(forms.ModelForm):
    """نموذج لإضافة تعليقات على صفحة تفاصيل النبات (Plant Detail)."""
    class Meta:
        model = Comment
        fields = ['full_name', 'content'] 
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'الاسم الكامل'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'اكتب تعليقك هنا...'}),
        }