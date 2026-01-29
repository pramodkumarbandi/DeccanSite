import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import User, OTP
from user.utils import validate_phone


@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    phone = request.data.get('phone')

    is_valid, msg = validate_phone(phone)
    if not is_valid:
        return Response({"error": msg}, status=400)

    try:
        user = User.objects.get(phone=phone)
        otp = random.randint(100000, 999999)

        OTP.objects.create(
            phone=phone,
            otp=str(otp),
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        return Response({"message": "OTP sent successfully"})

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    is_valid, msg = validate_phone(phone)
    if not is_valid:
        return Response({"error": msg}, status=400)

    if not otp or not new_password:
        return Response({"error": "OTP and new password are required"}, status=400)

    try:
        user = User.objects.get(phone=phone)

        otp_obj = OTP.objects.filter(phone=phone, otp=otp).last()

        if not otp_obj:
            return Response({"error": "Invalid OTP"}, status=400)

        if otp_obj.expires_at < timezone.now():
            return Response({"error": "OTP expired"}, status=400)

        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password reset successful"})

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
