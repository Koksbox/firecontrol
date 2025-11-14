# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('inspector', 'Инспектор'),
        ('viewer', 'Просмотр'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer',
        verbose_name="Роль"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Телефон"
    )

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"