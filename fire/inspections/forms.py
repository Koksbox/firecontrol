# inspections/forms.py
from django import forms
from .models import InspectionReport, InspectionPhoto

class InspectionReportForm(forms.ModelForm):
    class Meta:
        model = InspectionReport
        fields = ['fire_object', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 5}),
        }

class InspectionPhotoForm(forms.ModelForm):
    class Meta:
        model = InspectionPhoto
        fields = ['photo', 'caption']
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Описание фото (необязательно)'}),
        }