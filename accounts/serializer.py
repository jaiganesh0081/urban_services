from rest_framework import serializers

from .models import User, Role
from .validator import validate_username, validate_password_strong, validate_phone, validate_email, validate_role


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])
    password = serializers.CharField(validators=[validate_password_strong])
    phone = serializers.CharField(validators=[validate_phone])
    email = serializers.CharField(validators=[validate_email])
    role = serializers.CharField(validators=[validate_role])
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username','full_name', 'email', 'role', 'phone', 'password', 'confirm_password']
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True}
        }

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Password and Confirm password should be same")
        return data

    def create(self, validated_data):
        print("VALIDATED →", validated_data)
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')

        # FIX: convert role string → enum instance
        validated_data["role"] = Role(validated_data["role"])
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
