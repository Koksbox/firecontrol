# inspections/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import InspectionReport, InspectionPhoto
from .forms import InspectionReportForm, InspectionPhotoForm
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO



@login_required
def inspection_list(request):
    """Список всех проверок"""
    inspections = InspectionReport.objects.select_related('fire_object', 'inspector')
    return render(request, 'inspections/inspection_list.html', {'inspections': inspections})

@login_required
def inspection_create(request):
    """Создание нового акта проверки"""
    if request.method == "POST":
        form = InspectionReportForm(request.POST)
        if form.is_valid():
            inspection = form.save(commit=False)
            inspection.inspector = request.user
            inspection.save()
            return redirect('inspections:detail', pk=inspection.pk)
    else:
        form = InspectionReportForm()
    return render(request, 'inspections/inspection_form.html', {'form': form, 'title': 'Новая проверка'})

@login_required
def inspection_detail(request, pk):
    """Детали акта + управление фото"""
    inspection = get_object_or_404(InspectionReport, pk=pk)
    photos = inspection.photos.all()

    if request.method == "POST" and 'add_photo' in request.POST:
        photo_form = InspectionPhotoForm(request.POST, request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.inspection = inspection
            photo.save()
            return redirect('inspections:detail', pk=pk)
    else:
        photo_form = InspectionPhotoForm()

    return render(request, 'inspections/inspection_detail.html', {
        'inspection': inspection,
        'photos': photos,
        'photo_form': photo_form,
    })

@login_required
def inspection_complete(request, pk):
    """Завершить проверку (перевести в статус 'completed')"""
    inspection = get_object_or_404(InspectionReport, pk=pk)
    inspection.status = 'completed'
    inspection.save()
    # TODO: генерация PDF можно вызвать здесь
    return redirect('inspections:detail', pk=pk)

@login_required
def inspection_pdf(request, pk):
    inspection = get_object_or_404(InspectionReport, pk=pk)
    pdf = render_to_pdf('inspections/pdf_report.html', {'inspection': inspection})
    if pdf:
        return pdf
    return HttpResponse("Ошибка генерации PDF")

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None