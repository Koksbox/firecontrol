# objects/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import FireObject, ObjectType, ResponsiblePerson
from .forms import FireObjectForm
from django.db.models import Q

@login_required
def object_list(request):
    query = request.GET.get('q')
    type_filter = request.GET.get('type')
    class_filter = request.GET.get('class')

    objects = FireObject.objects.filter(is_archived=False)

    if query:
        objects = objects.filter(
            Q(name__icontains=query) |
            Q(actual_address__icontains=query) |
            Q(legal_address__icontains=query)
        )
    if type_filter:
        objects = objects.filter(object_type_id=type_filter)
    if class_filter:
        objects = objects.filter(fire_class=class_filter)

    object_types = ObjectType.objects.all()
    fire_classes = FireObject.FIRE_CLASSES

    return render(request, 'objects/object_list.html', {
        'objects': objects,
        'object_types': object_types,
        'fire_classes': fire_classes,
        'query': query,
        'type_filter': type_filter,
        'class_filter': class_filter,
    })

@login_required
def object_detail(request, pk):
    obj = get_object_or_404(FireObject, pk=pk)
    return render(request, 'objects/object_detail.html', {'object': obj})

@login_required
def object_create(request):
    if request.method == "POST":
        form = FireObjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('objects:list')
    else:
        form = FireObjectForm()
    return render(request, 'objects/object_form.html', {'form': form})

@login_required
def object_edit(request, pk):
    obj = get_object_or_404(FireObject, pk=pk)
    if request.method == "POST":
        form = FireObjectForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('objects:detail', pk=pk)
    else:
        form = FireObjectForm(instance=obj)
    return render(request, 'objects/object_form.html', {'form': form})

@login_required
def object_archive(request, pk):
    obj = get_object_or_404(FireObject, pk=pk)
    obj.is_archived = True
    obj.save()
    return redirect('objects:list')