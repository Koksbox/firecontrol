# objects/models.py
from django.db import models
from django.urls import reverse
from accounts.models import User

class ObjectType(models.Model):
    name = models.CharField("Тип объекта", max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип объекта"
        verbose_name_plural = "Типы объектов"

class FireObject(models.Model):
    FIRE_CLASSES = [
        ('F1.1', 'Ф1.1 — Детские дошкольные учреждения'),
        ('F1.2', 'Ф1.2 — Больницы'),
        ('F1.3', 'Ф1.3 — Жилые дома'),
        ('F1.4', 'Ф1.4 — Дома для престарелых'),
        ('F2.1', 'Ф2.1 — Театры, кинотеатры'),
        ('F2.2', 'Ф2.2 — Музеи, выставки'),
        ('F3.1', 'Ф3.1 — Торговые центры'),
        ('F3.2', 'Ф3.2 — Рестораны'),
        ('F3.3', 'Ф3.3 — Вокзалы'),
        ('F4.1', 'Ф4.1 — Образовательные учреждения'),
        ('F4.2', 'Ф4.2 — Научные учреждения'),
        ('F5.1', 'Ф5.1 — Производственные здания'),
        ('F5.2', 'Ф5.2 — Склады'),
    ]

    name = models.CharField("Наименование", max_length=255)
    legal_address = models.TextField("Юридический адрес")
    actual_address = models.TextField("Фактический адрес")
    object_type = models.ForeignKey(ObjectType, on_delete=models.PROTECT, verbose_name="Тип объекта")
    fire_class = models.CharField("Класс пожарной опасности", max_length=10, choices=FIRE_CLASSES)
    is_archived = models.BooleanField("В архиве", default=False)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('objects:detail', args=[self.pk])

    class Meta:
        verbose_name = "Объект надзора"
        verbose_name_plural = "Объекты надзора"


class ResponsiblePerson(models.Model):
    fire_object = models.ForeignKey(
        FireObject,
        on_delete=models.CASCADE,
        related_name='responsibles',
        verbose_name="Объект"
    )
    name = models.CharField("ФИО", max_length=200)
    position = models.CharField("Должность", max_length=200)
    phone_work = models.CharField("Рабочий телефон", max_length=20, blank=True)
    phone_mobile = models.CharField("Мобильный телефон", max_length=20, blank=True)
    email = models.EmailField("Email", blank=True)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Назначил"
    )
    assigned_at = models.DateTimeField("Назначен", auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.position})"

    class Meta:
        verbose_name = "Ответственное лицо"
        verbose_name_plural = "Ответственные лица"
        ordering = ['-assigned_at']