from uuid import uuid4

from django.db import models

from accounts.models import BaseModel
from providers.models import ProviderProfile, Category


class Service(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="services")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=200)
    description = models.TextField()
    base_fee = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration = models.IntegerField(help_text="Duration in minutes")

    class Meta:
        db_table = "service"

    def __str__(self):
        return f'{self.provider.user.full_name}-{self.title}'
