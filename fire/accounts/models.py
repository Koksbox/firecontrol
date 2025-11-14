# accounts/models.py (дополнить)
import hashlib
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('inspector', 'Инспектор'),
        ('viewer', 'Просмотр'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer', verbose_name="Роль")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")

    # PIN (не хранить plaintext!) — храним SHA256-хеш PIN'a
    pin_hash = models.CharField(max_length=64, blank=True, null=True, verbose_name="Хеш PIN")

    def set_pin(self, raw_pin: str):
        self.pin_hash = hashlib.sha256(raw_pin.encode('utf-8')).hexdigest()

    def check_pin(self, raw_pin: str) -> bool:
        if not self.pin_hash:
            return False
        return hashlib.sha256(raw_pin.encode('utf-8')).hexdigest() == self.pin_hash

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
