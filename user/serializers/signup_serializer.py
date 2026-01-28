from rest_framework import serializers
from ..models import User


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'username', 'password', 'confirm_password', 'campaign_code']
        extra_kwargs = {
            'campaign_code': {'required': False},
            'phone': {'validators': []}  # 🔥 remove auto unique validation
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords not matching"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
