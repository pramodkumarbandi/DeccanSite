import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.models import User, OTP


@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    """
    Step 1: User enters email -> send OTP
    """
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required"}, status=400)

    try:
        user = User.objects.get(email=email)
        otp = random.randint(100000, 999999)

        OTP.objects.create(
            user=user,
            otp=str(otp),
            expiry_time=timezone.now() + timedelta(minutes=5)
        )

        return Response({
            "message": "OTP sent successfully"
            # production lo otp return cheyyakudadhu
        })

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """
    Step 2: User enters OTP + new password
    """
    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    if not email or not otp or not new_password:
        return Response({"error": "All fields are required"}, status=400)

    try:
        user = User.objects.get(email=email)
        otp_obj = OTP.objects.filter(user=user, otp=otp).last()

        if not otp_obj:
            return Response({"error": "Invalid OTP"}, status=400)

        if otp_obj.expiry_time < timezone.now():
            return Response({"error": "OTP expired"}, status=400)

        user.password = make_password(new_password)
        user.save()

        return Response({"message": "Password reset successful"})

    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
