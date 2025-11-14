# documents/models.py
import os
from django.db import models
from django.urls import reverse
from objects.models import FireObject
from accounts.models import User

def document_upload_path(instance, filename):
    """Сохраняем файлы в: media/documents/<object_id>/<filename>"""
    return f'documents/object_{instance.fire_object_id}/{filename}'

class ObjectDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('evacuation_plan', 'Схема эвакуации'),
        ('equipment_plan', 'План размещения противопожарного инвентаря'),
        ('declaration', 'Декларация пожарной безопасности'),
        ('inspection_report', 'Отчёт о проверке'),
        ('other', 'Иной документ'),
    ]

    fire_object = models.ForeignKey(
        FireObject,
        on_delete=models.CASCADE,
        verbose_name="Объект надзора",
        related_name='documents'
    )
    title = models.CharField("Название документа", max_length=200)
    file = models.FileField(
        "Файл",
        upload_to=document_upload_path,
        help_text="Поддерживаемые форматы: PDF, JPG, PNG"
    )
    doc_type = models.CharField(
        "Тип документа",
        max_length=30,
        choices=DOC_TYPE_CHOICES
    )
    valid_until = models.DateField(
        "Действителен до",
        null=True,
        blank=True,
        help_text="Оставьте пустым, если бессрочный"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Загрузил"
    )
    uploaded_at = models.DateTimeField("Дата загрузки", auto_now_add=True)
    version = models.PositiveIntegerField("Версия", default=1, help_text="Для отслеживания обновлений")

    def __str__(self):
        return f"{self.title} ({self.get_doc_type_display()})"

    def get_absolute_url(self):
        return reverse('documents:detail', args=[self.pk])

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        verbose_name = "Документ объекта"
        verbose_name_plural = "Документы объектов"
        ordering = ['-uploaded_at']