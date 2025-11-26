from uuid import uuid4

from django.db import models

from accounts.models import BaseModel, User


# Create your models here.


class Category(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Skill(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = "skill"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProviderProfile(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="provider_profile")
    categories = models.ManyToManyField(Category, related_name="providers")
    experience = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)

    class Meta:
        db_table = 'provider_profile'

    def __str__(self):
        return self.user.full_name or self.user.username


class ProviderSkill(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='provider_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='skill_provider')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "skill"],
                name="unique_provider_skill"

            )
        ]

    def __str__(self):
        return f'{self.provider.user.full_name}-{self.skill.name}'


class Availabilty(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name="availability")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.provider.user.full_name}-{self.date}'
