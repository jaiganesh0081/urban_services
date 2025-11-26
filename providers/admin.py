from django.contrib import admin
from .models import Category, Skill, ProviderProfile
# Register your models here.
admin.site.register([Category, Skill, ProviderProfile])