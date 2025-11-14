# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('extinguisher_due', 'Проверка огнетушителя'),
        ('document_expired', 'Просроченный документ'),
        ('inspection_due', 'Плановая проверка'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Получатель")
    message = models.TextField("Текст уведомления")
    is_read = models.BooleanField("Прочитано", default=False)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    notification_type = models.CharField("Тип", max_length=30, choices=NOTIFICATION_TYPES)

    # Связь с объектом (например, огнетушителем или документом)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user}: {self.message[:50]}..."

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ['-created_at']