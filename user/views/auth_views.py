from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers.login_serializer import LoginSerializer
from user.serializers.signup_serializer import SignupSerializer
from user.utils import generate_otp
from user.models import User
from user.serializers.signup_serializer import SendOTPSerializer, VerifyOTPSerializer, SignupSerializer



# class LoginView(APIView):
#     authentication_classes = []
#     permission_classes = []
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "user_id": user.user_id,
#             "username": user.username,
#             "access": str(refresh.access_token),
#             "refresh": str(refresh)
#         }, status=status.HTTP_200_OK)
    


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #extract actual user object
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "user_id": str(user.user_id),
            "username": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


class SendOTPView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        user = User.objects.filter(phone=phone).first()
        if not user:
            # create inactive user to store OTP
            user = User.objects.create_user(username=f"user_{phone}", phone=phone, password="temporarypass")
            user.is_active = False
            user.save()

        otp = generate_otp()
        user.set_otp(otp)

        # TODO: integrate real SMS sending here
        print(f"Send OTP {otp} to phone {phone}")

        return Response({"message": f"OTP sent to {phone}"}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        otp = serializer.validated_data['otp']

        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        if user.verify_otp(otp):
            return Response({"message": "Phone verified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

class SignupView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user_id": str(user.user_id),
            "username": user.username,
            "phone": user.phone,
            "campaign_code": user.campaign_code
        }, status=status.HTTP_201_CREATED)
    