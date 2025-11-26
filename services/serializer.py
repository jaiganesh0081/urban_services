from django.db import transaction
from rest_framework import serializers

from providers.models import Category, Availabilty
from .models import Service


class ProviderServiceSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category",
                                                     write_only=True)
    category = serializers.CharField(source="category.id", read_only=True)

    class Meta:
        model = Service
        fields = ['title', 'description', 'category', 'category_id', 'base_fee', 'estimated_duration']

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user

        # This is a Category instance

        title = attrs.get('title')
        if not hasattr(user, "provider_profile"):
            raise serializers.ValidationError("Provider profile not found. Create profile first.")
        provider = request.user.provider_profile
        category = attrs.get("category")

        if category is None:
            raise serializers.ValidationError("Catergory field is required")

        if not provider.categories.filter(id=category.id).exists():
            raise serializers.ValidationError("Category is not belongs to provider")

        title = attrs.get('title', '').strip()
        if not title:
            raise serializers.ValidationError("Title is required")

        base_fee = attrs.get('base_fee')
        if base_fee is None or base_fee <= 0:
            raise serializers.ValidationError("Base fee must be greater than 0.")

        estimated_duration = attrs.get('estimated_duration')
        if estimated_duration is None or estimated_duration <= 0:
            raise serializers.ValidationError({"estimated_duration": "Estimated duration must be > 0 minutes."})
        if estimated_duration > 1000:
            raise serializers.ValidationError("Estimate duration is below the 1000 minutes")

        if Service.objects.filter(provider=provider, category=category).exists():
            raise serializers.ValidationError(
                "A service with the same category already exists for this provider and category.")

        attrs['title'] = title
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        provider = request.user.provider_profile
        category = validated_data.pop('category')
        try:
            with transaction.atomic():
                service = Service.objects.create(provider=provider, category=category, **validated_data)
                return service
        except Exception as e:
            raise serializers.ValidationError(str(e))


class ServiceSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.user.full_name', read_only=True)
    provider_rating = serializers.DecimalField(source="provider.rating_avg", decimal_places=2, max_digits=3,
                                               read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'title', 'base_fee', 'estimated_duration', 'provider_name', 'provider_rating']


class ServiceSerializer(serializers.ModelSerializer):
    # provider_name = serializers.CharField(source='provider.user.full_name', read_only=True)
    # provider_rating = serializers.DecimalField(source='provider.rating_avg', max_digits=3, decimal_places=2,
    #                                            read_only=True)
    provider = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "description",
            "base_fee",
            "estimated_duration",
            "provider"
        ]

    def get_provider(self, data):
        availability = data.provider.availability.all()

        return {
            "provider_id": data.provider.id,
            "provider_name": data.provider.user.full_name,
            "provider_rating": data.provider.rating_avg,
            "Available": [{"availabilty_id": avail.id,
                           "date": avail.date,
                           "start_time": avail.start_time,
                           "end_time": avail.end_time
                           } for avail in availability]
        }


class CategoryGroupSerializer(serializers.Serializer):
    category_id = serializers.UUIDField()
    category_name = serializers.CharField()
    services = ServiceSerializer(many=True)
