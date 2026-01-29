import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..models import User, OTP
from ..serializers.signup_serializer import RegisterSerializer   # ✅ (1) ADD THIS


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
def resend_otp(request):
    phone = request.data.get('phone')

    if not phone:
        return Response({"error": "Phone number required"}, status=400)

    OTP.objects.filter(phone=phone).delete()

    otp = str(random.randint(100000, 999999))
    expiry = timezone.now() + timedelta(minutes=5)

    OTP.objects.create(phone=phone, otp=otp, expires_at=expiry)

    print("Resent OTP:", otp)
    return Response({"message": "OTP resent successfully"})


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

    # 🔹 (2) OTP verification unchanged
    otp_obj = OTP.objects.filter(phone=phone, is_verified=True).first()
    if not otp_obj:
        return Response({"error": "OTP not verified"}, status=400)

    user = User.objects.filter(phone=phone).first()

    if user and user.has_usable_password():
        return Response(
            {"error": "This phone number is already registered. Please login."},
            status=400
        )

    # 🔥 (3) SERIALIZER VALIDATION ADDED
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    # 🔹 (4) User exists but password not set (OTP signup flow)
    if user and not user.has_usable_password():
        user.username = serializer.validated_data['username']
        user.set_password(serializer.validated_data['password'])
        user.campaign_code = serializer.validated_data.get('campaign_code')
        user.save()
        return Response({"message": "Registration completed successfully"}, status=200)

    # 🔹 (5) New user creation (serializer handles password validation + hashing)
    serializer.save()
    return Response({"message": "User registered successfully"}, status=201)
