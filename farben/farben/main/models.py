from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class SellerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Seller(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'  # Используем email для входа вместо username
    REQUIRED_FIELDS = []      # Дополнительные обязательные поля (не нужны)

    objects = SellerManager()

    def __str__(self):
        return self.name
    
class INNField(models.CharField):
    description = "Поле для хранения ИНН"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 12)
        kwargs.setdefault('unique', True)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["unique"]
        return name, path, args, kwargs
    

class Client(models.Model):
    class Meta:
        verbose_name = _("Клиент")
        verbose_name_plural = _("Клиенты")
        ordering = ['last_name', 'first_name']
    
    # Основные поля
    inn = models.CharField(
        _("ИНН"),
        max_length=12,
        unique=True,
        help_text=_("10 или 12 цифр")
    )
    last_name = models.CharField(
        _("Фамилия"),
        max_length=150
    )
    first_name = models.CharField(
        _("Имя"),
        max_length=150
    )
    middle_name = models.CharField(
        _("Отчество"),
        max_length=150,
        blank=True,
        null=True
    )
    
    # Служебные поля
    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True
    )

    def __str__(self):
        return f"{self.full_name} (ИНН: {self.inn})"

    @property
    def full_name(self):
        """Возвращает полное ФИО"""
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return " ".join(parts)

    def clean(self):
        """Валидация данных перед сохранением"""
        super().clean()
        
        # Проверка ИНН
        if not self.inn.isdigit():
            raise ValidationError({'inn': _("ИНН должен содержать только цифры")})
        
        if len(self.inn) not in [10, 12]:
            raise ValidationError({'inn': _("ИНН должен содержать 10 или 12 цифр")})

    def save(self, *args, **kwargs):
        """Переопределение метода сохранения"""
        self.full_clean()  # Принудительная валидация при сохранении
        super().save(*args, **kwargs)