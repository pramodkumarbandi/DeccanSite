from rest_framework import serializers
from user.models import User

class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    campaign_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'phone', 'password', 'confirm_password', 'campaign_code']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        # Check if phone is verified
        phone = data.get('phone')
        user = User.objects.filter(phone=phone).first()
        if not user or not user.is_verified:
            raise serializers.ValidationError("Phone number not verified")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        campaign_code = validated_data.pop('campaign_code', None)
        user = User.objects.get(phone=validated_data['phone'])
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        if campaign_code:
            user.campaign_code = campaign_code
        user.is_active = True
        user.save()
        return user
