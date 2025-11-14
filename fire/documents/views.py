# documents/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import ObjectDocument
from .forms import ObjectDocumentForm

@login_required
def document_list(request):
    """Список всех документов"""
    documents = ObjectDocument.objects.select_related('fire_object', 'uploaded_by')
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_detail(request, pk):
    """Детали документа"""
    doc = get_object_or_404(ObjectDocument, pk=pk)
    return render(request, 'documents/document_detail.html', {'document': doc})

@login_required
def document_create(request):
    """Загрузка нового документа"""
    if request.method == "POST":
        form = ObjectDocumentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('documents:list')
    else:
        form = ObjectDocumentForm(user=request.user)
    return render(request, 'documents/document_form.html', {'form': form, 'title': 'Загрузить документ'})

@login_required
def document_delete(request, pk):
    """Удаление документа"""
    doc = get_object_or_404(ObjectDocument, pk=pk)
    if request.method == "POST":
        doc.file.delete(save=False)  # удаляем файл с диска
        doc.delete()
        return redirect('documents:list')
    return render(request, 'documents/document_confirm_delete.html', {'document': doc})