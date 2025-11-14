# objects/forms.py
from django import forms
from .models import FireObject

class FireObjectForm(forms.ModelForm):
    class Meta:
        model = FireObject
        fields = ['name', 'legal_address', 'actual_address', 'object_type', 'fire_class']
        widgets = {
            'legal_address': forms.Textarea(attrs={'rows': 2}),
            'actual_address': forms.Textarea(attrs={'rows': 2}),
        }