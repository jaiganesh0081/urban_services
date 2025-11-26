from rest_framework import serializers

from providers.models import Availabilty


class ProviderAvailableSerializer(serializers.ModelSerializer):
    provider_id = serializers.UUIDField(source="provider.id")
    provider_name = serializers.CharField(source="provider.user.full_name")

    class Meta:
        model = Availabilty
        fields = ["id", "provider_id", "provider_name", "date", "start_time", "end_time"]
        read_only_fields = fields
