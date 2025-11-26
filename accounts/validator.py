from rest_framework import serializers

from .models import User, Role


def validate_username(value):
    if not value:
        raise serializers.ValidationError("Username is required for Registrations and Username is consider as name")
    if User.objects.filter(username__iexact=value).exists():
        raise serializers.ValidationError("Username is already registered")
    if value.lower() == 'admin' or value.lower() == 'superadmin':
        raise serializers.ValidationError("Username should not contain admin or superadmin")
    length = len(value)
    if length <= 5:
        raise serializers.ValidationError('Username is less than 5 Characters ')
    return value


def validate_password_strong(value):
    if not value:
        raise serializers.ValidationError("Password is required")
    if len(value) < 8:
        raise serializers.ValidationError("Password should have minimum 8 characters")
    if not any(char.isdigit() for char in value):
        raise serializers.ValidationError("Password should contain atleast one digit")
    special_char = "@#$%^&*!"
    if not any(char in special_char for char in value):
        raise serializers.ValidationError("Password should contain atleast one special character")
    return value


def validate_phone(value):
    length = len(value)
    if not 10 <= length <= 15:
        raise serializers.ValidationError("Phone number should 10-15 digits")
    if not value.isdigit():
        raise serializers.ValidationError("Phone number should not contails any Characters")
    if not value.startswith(("9", "6")):
        raise serializers.ValidationError("Phone number need to starts with 9 or 6")
    return value


def validate_email(value):
    if User.objects.filter(email__iexact=value).exists():
        raise serializers.ValidationError("Email address already exists ")
    return value


def validate_role(value):
    if not value:
        raise serializers.ValidationError("Role field is required")

    value = value.title()
    print(f'the customer is {value}')

    # FIX: Return exactly TextChoices values
    if value == "Customer":
        return Role.Customer
    if value == "Provider":
        return Role.Provider

    raise serializers.ValidationError("Role must be Customer or Provider")
