from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.utils import timezone


# Create your models here.


class Status(models.TextChoices):
    Active = "Active", "Active"
    Inactive = "Inactive", "Inactive"


class Role(models.TextChoices):
    Customer = "Customer", "Customer"
    Provider = "Provider", "Provider"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # abstract is True when we use this for models have these fields
        abstract = True
        ordering = ['-created_at']


class UserCounter(models.Model):
    role = models.CharField(max_length=20, choices=Role.choices)
    year = models.IntegerField()
    counter = models.IntegerField(default=0)

    class Meta:
        unique_together = ("role", "year")

    def __str__(self):
        return f'{self.role}-{self.year}-{self.counter}'


class User(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    full_name = models.CharField(max_length=150, null=True, blank=True)
    user_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.Customer)
    phone = models.CharField(max_length=15, null=True, blank=True)

    @staticmethod
    def built_customer_code(year: int, new_number: int) -> str:
        return f'CUS{year}{new_number:07d}'

    @staticmethod
    def built_provider_code(year: int, new_number: int) -> str:
        return f'PRO{year}{new_number:07d}'

    @classmethod
    def get_next_number(cls, role):
        year = timezone.now().year

        with transaction.atomic():
            counter_obj, created = UserCounter.objects.select_for_update().get_or_create(
                role=role,
                year=year,
                defaults={"counter": 0}
            )
            counter_obj.counter += 1
            counter_obj.save()
            return year, counter_obj.counter

    @classmethod
    def generate_customer_code(cls):
        year, counter = cls.get_next_number(Role.Customer)
        return cls.built_customer_code(year, counter)

    @classmethod
    def generate_provider_code(cls):
        year, counter = cls.get_next_number(Role.Provider)
        return cls.built_provider_code(year, counter)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            super().save(*args, **kwargs)
            return

        if not self.user_code:
            if self.role == Role.Customer:
                self.user_code = self.generate_customer_code()
            elif self.role == Role.Provider:
                self.user_code = self.generate_provider_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username}-{self.role}-{self.user_code}'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user_registration"
