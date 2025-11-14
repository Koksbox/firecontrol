# notifications/tasks.py
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from fire_safety.models import FireExtinguisher
from documents.models import ObjectDocument
from datetime import timedelta
from django.core.management.base import BaseCommand
from notifications.tasks import send_upcoming_deadline_notifications
User = get_user_model()



class Command(BaseCommand):
    help = 'Отправляет уведомления о предстоящих и просроченных сроках'

    def handle(self, *args, **options):
        self.stdout.write('Проверка сроков и отправка уведомлений...')
        send_upcoming_deadline_notifications()
        self.stdout.write(
            self.style.SUCCESS('Уведомления отправлены успешно!')
        )

def send_upcoming_deadline_notifications():
    """
    Отправляет email-уведомления:
    - За 3 дня до проверки огнетушителя
    - О просроченных/истекающих документах
    """
    today = timezone.now().date()
    deadline_date = today + timedelta(days=3)

    # 1. Огнетушители — проверка через 3 дня
    extinguishers = FireExtinguisher.objects.filter(
        next_check_date=deadline_date,
        is_active=True
    ).select_related('fire_object')

    for ext in extinguishers:
        admins = User.objects.filter(role='admin')
        for admin in admins:
            if not admin.email:
                continue
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
                fail_silently=True,
            )

    # 2. Документы — просрочены или истекают завтра
    expired_docs = ObjectDocument.objects.filter(
        valid_until__isnull=False,
        valid_until__lte=today + timedelta(days=1)
    ).select_related('fire_object')

    for doc in expired_docs:
        admins = User.objects.filter(role='admin')
        for admin in admins:
            if not admin.email:
                continue
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
                fail_silently=True,
            )