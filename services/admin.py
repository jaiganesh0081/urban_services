from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "provider",
        "base_fee",
        "estimated_duration",
        "created_at",
    )

    list_filter = (
        "category",
        "provider__user__full_name",
        "base_fee",
    )

    search_fields = (
        "title",
        "description",
        "provider__user__full_name",
    )

    ordering = ("category", "title")

    list_per_page = 20
