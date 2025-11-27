# plants/forms.py
from django import forms
from .models import Plant, Country, Comment

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = '__all__'
        
        # هنا السر: نحدد أي حقل نريد تنسيقه
        widgets = {
            # 1. تحديد حقل الدول (Countries)
            'countries': forms.SelectMultiple(attrs={
                'class': 'form-control select2-multi',  # <--- هذا الكلاس هو المسؤول
                'style': 'width: 100%',
            }),
            
            # 2. (اختياري) تحسين شكل باقي الحقول لتصبح مثل "Category"
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'used_for': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}), # إذا كان قائمة
        }

class PlantForm(forms.ModelForm):
    # اختيار عدة بلدان للنبات (اختياري)
    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(),
        required=False,
        label="Countries",
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
        # لو تحبها مربعات اختيار استخدم:
        # widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Plant
        fields = ["name", "about", "used_for", "image", "category", "is_edible", "countries"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Plant name", "class": "form-control"}),
            "about": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "used_for": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            # image يكتفي بويدجت الافتراضي لحقل الصور
            "is_edible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class PlantSearchForm(forms.Form):
    search = forms.CharField(required=False, label="Search",
                             widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title or content..."}))
    category = forms.ChoiceField(
        required=False,
        choices=[("", "All")] + list(Plant.Category.choices),
        label="Category",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    is_edible = forms.ChoiceField(
        required=False,
        choices=[("", "Unknown"), ("true", "Edible"), ("false", "Not edible")],
        label="Edible?",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        empty_label="All",
        label="Country",
        widget=forms.Select(attrs={"class": "form-control"})
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "content"]
        labels = {
            "name": "Name",
            "content": "Comment",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "class": "form-control"}),
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Write your comment...",
                "class": "form-control",
            }),
        }
