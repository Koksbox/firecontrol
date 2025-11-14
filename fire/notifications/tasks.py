# notifications/tasks.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from fire_safety.models import FireExtinguisher
from documents.models import ObjectDocument
from datetime import timedelta

User = get_user_model()

def send_upcoming_deadline_notifications():
    """
    Отправляет уведомления за 3, 14 и 30 дней до срока.
    Для MVP — только за 3 дня.
    """
    today = timezone.now().date()
    deadline_date = today + timedelta(days=3)

    # 1. Огнетушители
    extinguishers = FireExtinguisher.objects.filter(
        next_check_date=deadline_date,
        is_active=True
    ).select_related('fire_object')

    for ext in extinguishers:
        # Определяем получателя: админ или инспектор (временно — всех админов)
        admins = User.objects.filter(role='admin')
        for admin in admins:
            subject = f"Напоминание: проверка огнетушителя на {ext.fire_object.name}"
            message = f"""
            На объекте "{ext.fire_object.name}" (адрес: {ext.fire_object.actual_address})
            требуется проверка огнетушителя №{ext.inventory_number} ({ext.get_type_display()}).

            Следующая проверка: {ext.next_check_date}.
            Место установки: {ext.location}

            Пожарный контроль: Стерлитамак
            """
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin.email],
                fail_silently=False,
            )

    # 2. Документы (просроченные сегодня или завтра)
    expired_docs = ObjectDocument.objects.filter(
        valid_until__isnull=False,
        valid_until__lte=today + timedelta(days=1)
    ).select_related('fire_object', 'uploaded_by')

    for doc in expired_docs:
        admins = User.objects.filter(role='admin')
        for admin in admins:
            subject = f"Внимание: документ просрочен на {doc.fire_object.name}"
            message = f"""
            Документ "{doc.title}" ({doc.get_doc_type_display()}) на объекте "{doc.fire_object.name}"
            просрочен или истекает завтра ({doc.valid_until}).

            Пожалуйста, обновите схему или декларацию.

            Пожарный контроль: Стерлитамак
            """
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin.email],
                fail_silently=False,
            )