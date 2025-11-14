# fire_safety/forms.py
from django import forms
from .models import FireExtinguisher

class FireExtinguisherForm(forms.ModelForm):
    class Meta:
        model = FireExtinguisher
        fields = [
            'fire_object', 'inventory_number', 'type',
            'location', 'last_refill_date', 'next_check_date'
        ]
        widgets = {
            'last_refill_date': forms.DateInput(attrs={'type': 'date'}),
            'next_check_date': forms.DateInput(attrs={'type': 'date'}),
        }