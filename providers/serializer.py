from django.db import transaction
from rest_framework import serializers
from bookings.models import Booking
from .models import ProviderProfile, ProviderSkill, Skill, Availabilty, Category


class ProviderProfileSerializer(serializers.ModelSerializer):
    skill_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    # Return list of category IDs
    categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProviderProfile
        fields = ["categories", "skill_ids", "experience", "address"]

    def get_categories(self, obj):
        return [str(cat.id) for cat in obj.categories.all()]

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user

        if hasattr(user, 'provider_profile'):
            return serializers.ValidationError("Provider profile is already exists")

        skill_ids = attrs.get("skill_ids", [])
        skills = Skill.objects.filter(id__in=skill_ids)

        # Check if all skill_ids are valid
        if len(skill_ids) != skills.count():
            raise serializers.ValidationError("One or more skills are invalid.")

        return attrs

    def create(self, validated_data):
        skill_ids = validated_data.pop("skill_ids")
        request = self.context.get("request")
        user = request.user

        # Fetch all skill objects
        skills = Skill.objects.filter(id__in=skill_ids)

        # Auto-detect category IDs from skills
        category_ids = {skill.category_id for skill in skills}

        try:
            with transaction.atomic():
                # Create profile
                profile = ProviderProfile.objects.create(
                    user=user,
                    **validated_data
                )

                # Assign categories automatically
                profile.categories.set(category_ids)

                # Save skills
                for skill in skills:
                    ProviderSkill.objects.create(
                        provider=profile,
                        skill=skill
                    )

                return profile

        except Exception as e:
            raise serializers.ValidationError(str(e))


class ProviderSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availabilty
        fields = ["date", "start_time", "end_time"]

    def validate(self, attrs):
        request = self.context["request"]
        provider = request.user.provider_profile

        date = attrs.get("date")
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        if end_time <= start_time:
            raise serializers.ValidationError("end_time must be after start_time")
        exists = Availabilty.objects.filter(
            provider=provider,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if exists:
            raise serializers.ValidationError(
                "This time slot overlaps with an existing slot"
            )
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        provider = request.user.provider_profile
        try:
            availability = Availabilty.objects.create(provider=provider, **validated_data)
            return availability
        except Exception as e:
            raise serializers.ValidationError(str(e))


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    class Meta:
        model = Category
        fields = ["id", "name", "skills"]
