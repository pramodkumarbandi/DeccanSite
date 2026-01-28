import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import User, OTP


@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    phone = request.data.get('phone')

    if not phone:
        return Response({"error": "Phone number required"}, status=400)

    otp = str(random.randint(100000, 999999))
    expiry = timezone.now() + timedelta(minutes=5)

    OTP.objects.filter(phone=phone).delete()
    OTP.objects.create(phone=phone, otp=otp, expires_at=expiry)

    print("OTP:", otp)

    return Response({"message": "OTP sent successfully"})


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')

    otp_obj = OTP.objects.filter(phone=phone).first()

    if not otp_obj:
        return Response({"error": "OTP not found"}, status=400)

    if otp_obj.is_expired():
        otp_obj.delete()
        return Response({"error": "OTP expired"}, status=400)

    if otp_obj.otp != otp:
        return Response({"error": "Invalid OTP"}, status=400)

    otp_obj.is_verified = True
    otp_obj.save()

    return Response({"message": "OTP verified successfully"})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    phone = request.data.get('phone')
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    campaign_code = request.data.get('campaign_code')

    if password != confirm_password:
        return Response({"error": "Passwords do not match"}, status=400)

    otp_obj = OTP.objects.filter(phone=phone, is_verified=True).first()
    if not otp_obj:
        return Response({"error": "OTP not verified"}, status=400)

    user = User.objects.filter(phone=phone).first()

    if user and user.has_usable_password():
        return Response(
            {"error": "This phone number is already registered. Please login."},
            status=400
        )

    if user and not user.has_usable_password():
        user.username = username
        user.password = make_password(password)
        user.campaign_code = campaign_code
        user.save()
        return Response({"message": "Registration completed successfully"}, status=200)

    User.objects.create(
        phone=phone,
        username=username,
        password=make_password(password),
        campaign_code=campaign_code
    )

    return Response({"message": "User registered successfully"}, status=201)
