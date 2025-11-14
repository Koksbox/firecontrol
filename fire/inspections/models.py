# inspections/models.py
import os
from django.db import models
from django.urls import reverse
from accounts.models import User
from objects.models import FireObject

def inspection_photo_upload_path(instance, filename):
    """Сохраняем фото: media/inspections/<inspection_id>/photos/<filename>"""
    return f'inspections/{instance.inspection.id}/photos/{filename}'

class InspectionReport(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('completed', 'Завершён'),
    ]

    fire_object = models.ForeignKey(
        FireObject,
        on_delete=models.CASCADE,
        verbose_name="Объект надзора",
        related_name='inspections'
    )
    inspector = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Инспектор"
    )
    date = models.DateField("Дата проверки")
    notes = models.TextField("Замечания", blank=True, help_text="Опишите выявленные нарушения")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='draft')
    pdf_file = models.FileField("PDF-акт", upload_to='inspections/pdfs/', null=True, blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    def __str__(self):
        return f"Проверка {self.fire_object.name} от {self.date}"

    def get_absolute_url(self):
        return reverse('inspections:detail', args=[self.pk])

    class Meta:
        verbose_name = "Акт проверки"
        verbose_name_plural = "Акты проверок"
        ordering = ['-date']

class InspectionPhoto(models.Model):
    inspection = models.ForeignKey(
        InspectionReport,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo = models.ImageField("Фотография", upload_to=inspection_photo_upload_path)
    caption = models.CharField("Подпись", max_length=200, blank=True)

    def __str__(self):
        return f"Фото к проверке {self.inspection.id}"

    def filename(self):
        return os.path.basename(self.photo.name)

    class Meta:
        verbose_name = "Фото нарушения"
        verbose_name_plural = "Фото нарушений"