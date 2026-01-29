import re
from rest_framework import serializers
from ..models import User


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'username', 'password', 'confirm_password', 'campaign_code']
        extra_kwargs = {
            'password': {'write_only': True},
            'campaign_code': {'required': False},
            'phone': {'validators': []}
        }

    def validate_phone(self, value):
        if not re.fullmatch(r'[6-9]\d{9}', value):
            raise serializers.ValidationError("Enter valid 10 digit mobile number")

        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number already registered")

        return value

    def validate_username(self, value):
        if not re.fullmatch(r'^[a-zA-Z0-9_]{4,30}$', value):
            raise serializers.ValidationError(
                "Username must be 4–30 characters and contain only letters, numbers, underscore"
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")

        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain 1 uppercase letter")

        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain 1 lowercase letter")

        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain 1 number")

        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise serializers.ValidationError("Password must contain 1 special character")

        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
