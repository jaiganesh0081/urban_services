from rest_framework import serializers

from providers.models import Availabilty, Skill, Category


class ProviderAvailableSerializer(serializers.ModelSerializer):
    provider_id = serializers.UUIDField(source="provider.id")
    provider_name = serializers.CharField(source="provider.user.full_name")

    class Meta:
        model = Availabilty
        fields = ["id", "provider_id", "provider_name", "date", "start_time", "end_time"]
        read_only_fields = fields


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "skills"]
