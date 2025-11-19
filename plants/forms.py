
from django import forms
from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "about", "used_for", "image", "category", "is_edible"]


# plants/forms.py
from django import forms
from .models import Plant

class PlantSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search plants..."})
    )
    category = forms.ChoiceField(
        required=False,
        choices=[("", "All categories")] + list(Plant.Category.choices),
        label="Category"
    )
    is_edible = forms.ChoiceField(
        required=False,
        choices=[
            ("", "All"),
            ("true", "Edible"),
            ("false", "Not edible"),
        ],
        label="Is edible"
    )
# End of plants/forms.py

