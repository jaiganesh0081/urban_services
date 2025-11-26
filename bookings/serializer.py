import datetime

from rest_framework import serializers

from providers.models import ProviderProfile, Availabilty
from services.models import Service
from .models import Booking


class BookingServicesSerializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), source="service", write_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(queryset=ProviderProfile.objects.all(), source="provider",
                                                     write_only=True)

    class Meta:
        model = Booking
        fields = ["service_id", "provider_id", "date", "start_time", "end_time"]

    def validate(self, attrs):
        service = attrs["service"]
        provider = attrs["provider"]
        date = attrs["date"]
        start_time = attrs["start_time"]
        end_time = attrs["end_time"]
        today = datetime.date.today()

        if service.provider_id != provider.id:
            raise serializers.ValidationError("This service does not belong to this provider.")
        if date < today:
            raise serializers.ValidationError("You cannot book a past date.")
        if end_time <= start_time:
            raise serializers.ValidationError("end_time must be after start_time.")
        available = Availabilty.objects.filter(provider=provider, date=date, start_time__lte=start_time,
                                               end_time__gte=end_time).exists()
        if not available:
            raise serializers.ValidationError("Provider is not available during this time.")
        conflict = Booking.objects.filter(
            provider=provider,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()
        if conflict:
            raise serializers.ValidationError("Provider already has a booking that conflicts with this time.")
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        customer = request.user
        try:
            booking = Booking.objects.create(customer=customer, **validated_data)
            return booking
        except Exception as e:
            raise serializers.ValidationError(str(e))


class CustomerSerializer(serializers.Serializer):
    customer_id = serializers.UUIDField(source="id")
    customer_name = serializers.CharField(source="full_name")


class ServiceSerializer(serializers.Serializer):
    service_id = serializers.UUIDField(source="id")
    title = serializers.CharField()
    description = serializers.CharField()


class ProviderBookingSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Booking
        fields = [
            "id",
            "date",
            "start_time",
            "end_time",
            "status",
            "customer",
            "service",
        ]
        read_only_fields = ["id", "customer", "service", "date", "start_time", "end_time"]

    def validate(self, attrs):
        status = self.initial_data.get("status")
        if not status:
            raise serializers.ValidationError("status field is required")
        allowed_status = ["Accepted","Rejected","Completed"]
        if status not in allowed_status:
            raise serializers.ValidationError("Invalid status value")

        instance = self.instance  # booking instance

        # Transition rules
        valid_transitions = {
            "Pending": ["Accepted", "Rejected"],
            "Accepted": ["Completed"],
            "Rejected": [],
            "Completed": []
        }

        if status not in valid_transitions[instance.status]:
            raise serializers.ValidationError(
                {"status": f"Cannot change status from {instance.status} to {status}"}
            )

        return {"status": status}

    def update(self, instance, validated_data):
        instance.status = validated_data["status"]
        instance.save()
        return instance
