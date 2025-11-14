# normative/models.py
from django.db import models

class NormativeDocument(models.Model):
    title = models.CharField("Название", max_length=300)
    doc_number = models.CharField("Номер", max_length=100, blank=True)
    issue_date = models.DateField("Дата принятия", null=True, blank=True)
    file = models.FileField("Файл (PDF)", upload_to='normative/', blank=True)
    url = models.URLField("Ссылка", blank=True, help_text="Если документ онлайн")
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Нормативный документ"
        verbose_name_plural = "Нормативные документы"
        ordering = ['-issue_date']