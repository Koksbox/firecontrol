# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from objects.models import FireObject
from fire_safety.models import FireExtinguisher
from documents.models import ObjectDocument
from inspections.models import InspectionReport

@login_required
def dashboard_view(request):
    user = request.user
    today = timezone.now().date()

    # 1. Общая статистика
    total_objects = FireObject.objects.count()
    active_objects = FireObject.objects.filter(is_archived=False).count()

    # 2. Критичные огнетушители (просроченные ИЛИ проверка в ближайшие 3 дня)
    critical_extinguishers = FireExtinguisher.objects.filter(
        is_active=True,
        next_check_date__lte=today + timedelta(days=3)
    ).select_related('fire_object').order_by('next_check_date')

    # 3. Просроченные документы
    expired_documents = ObjectDocument.objects.filter(
        valid_until__isnull=False,
        valid_until__lt=today
    ).select_related('fire_object')

    # 4. Последние проверки (последние 5)
    recent_inspections = InspectionReport.objects.select_related(
        'fire_object', 'inspector'
    ).order_by('-date')[:5]

    # 5. Объекты без ответственных (если будет модель ResponsiblePerson — добавим)
    # Пока пропустим

    context = {
        'total_objects': total_objects,
        'active_objects': active_objects,
        'critical_extinguishers': critical_extinguishers,
        'expired_documents': expired_documents,
        'recent_inspections': recent_inspections,
    }
    return render(request, 'dashboard/index.html', context)