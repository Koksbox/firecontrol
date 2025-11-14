# normative/views.py
from django.shortcuts import render
from .models import NormativeDocument

def normative_list(request):
    docs = NormativeDocument.objects.all()
    return render(request, 'normative/list.html', {'documents': docs})