# fire_safety/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FireExtinguisher
from .forms import FireExtinguisherForm

@login_required
def extinguisher_list(request):
    """Список всех огнетушителей (активных)"""
    extinguishers = FireExtinguisher.objects.filter(is_active=True).select_related('fire_object')
    return render(request, 'fire_safety/extinguisher_list.html', {'extinguishers': extinguishers})

@login_required
def extinguisher_detail(request, pk):
    """Карточка огнетушителя"""
    extinguisher = get_object_or_404(FireExtinguisher, pk=pk)
    return render(request, 'fire_safety/extinguisher_detail.html', {'extinguisher': extinguisher})

@login_required
def extinguisher_create(request):
    """Добавление нового огнетушителя"""
    if request.method == "POST":
        form = FireExtinguisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fire_safety:list')
    else:
        form = FireExtinguisherForm()
    return render(request, 'fire_safety/extinguisher_form.html', {'form': form, 'title': 'Добавить огнетушитель'})

@login_required
def extinguisher_edit(request, pk):
    """Редактирование огнетушителя"""
    extinguisher = get_object_or_404(FireExtinguisher, pk=pk)
    if request.method == "POST":
        form = FireExtinguisherForm(request.POST, instance=extinguisher)
        if form.is_valid():
            form.save()
            return redirect('fire_safety:detail', pk=pk)
    else:
        form = FireExtinguisherForm(instance=extinguisher)
    return render(request, 'fire_safety/extinguisher_form.html', {'form': form, 'title': 'Редактировать огнетушитель'})

@login_required
def extinguisher_deactivate(request, pk):
    """Деактивировать (вывести из эксплуатации)"""
    extinguisher = get_object_or_404(FireExtinguisher, pk=pk)
    extinguisher.is_active = False
    extinguisher.save()
    return redirect('fire_safety:list')