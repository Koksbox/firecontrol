# documents/forms.py
from django import forms
from .models import ObjectDocument

class ObjectDocumentForm(forms.ModelForm):
    class Meta:
        model = ObjectDocument
        fields = ['fire_object', 'title', 'file', 'doc_type', 'valid_until']
        widgets = {
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.instance.uploaded_by = user