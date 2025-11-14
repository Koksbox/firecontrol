# fire_safety/models.py
from django.db import models
from django.urls import reverse
from objects.models import FireObject

class FireExtinguisher(models.Model):
    TYPE_CHOICES = [
        ('powder', 'Порошковый'),
        ('co2', 'Углекислотный'),
        ('foam', 'Пенный'),
        ('water', 'Водный'),
        ('halon', 'Хладоновый'),
    ]

    fire_object = models.ForeignKey(
        FireObject,
        on_delete=models.CASCADE,
        verbose_name="Объект надзора",
        related_name='extinguishers'
    )
    inventory_number = models.CharField(
        "Инвентарный номер",
        max_length=100,
        unique=True,
        help_text="Уникальный номер по реестру"
    )
    type = models.CharField(
        "Тип огнетушителя",
        max_length=20,
        choices=TYPE_CHOICES
    )
    location = models.CharField(
        "Место установки",
        max_length=255,
        help_text="Например: 1-й этаж, коридор у входа"
    )
    last_refill_date = models.DateField(
        "Дата последней заправки",
        help_text="Когда был заправлен или освидетельствован"
    )
    next_check_date = models.DateField(
        "Дата следующей проверки",
        help_text="Когда требуется следующая проверка/заправка"
    )
    is_active = models.BooleanField(
        "Активен",
        default=True,
        help_text="Снимите галочку, если выведен из эксплуатации"
    )
    created_at = models.DateTimeField("Добавлен", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    def __str__(self):
        return f"Огнетушитель №{self.inventory_number} ({self.get_type_display()})"

    def get_absolute_url(self):
        return reverse('fire_safety:detail', args=[self.pk])

    class Meta:
        verbose_name = "Огнетушитель"
        verbose_name_plural = "Огнетушители"
        ordering = ['next_check_date']