from rest_framework import serializers
from ..models import User
from user.utils import validate_phone

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'username', 'password', 'confirm_password', 'campaign_code']
        extra_kwargs = {
            'password': {'write_only': True},
            'campaign_code': {'required': False},
            'phone': {'validators': []},  # disable default unique validator
        }

    def validate_phone(self, value):
        is_valid, message = validate_phone(value)
        if not is_valid:
            raise serializers.ValidationError(message)

        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number already registered")

        return value

    def validate_username(self, value):
        if len(value) < 4 or len(value) > 30:
            raise serializers.ValidationError(
                "Username must be 4–30 characters long"
            )

        if not value.replace("_", "").isalnum():
            raise serializers.ValidationError(
                "Username can contain only letters, numbers, and underscore"
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")

        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain 1 uppercase letter")

        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain 1 lowercase letter")

        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain 1 number")

        if not any(char in "!@#$%^&*(),.?\":{}|<>" for char in value):
            raise serializers.ValidationError("Password must contain 1 special character")

        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
