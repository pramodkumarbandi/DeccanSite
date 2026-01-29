from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    login_type = request.data.get("login_type", "normal")  #  ADD
    identifier = request.data.get("identifier")            # username or phone
    password = request.data.get("password")

    # DEMO LOGIN FLOW
    if login_type == "demo":
        demo_user = User.objects.filter(username="demo_user").first()
        if not demo_user:
            return Response(
                {"error": "Demo user not configured"},
                status=400
            )

        refresh = RefreshToken.for_user(demo_user)
        return Response({
            "message": "Demo login successful",
            "user_type": "demo",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=200)

    # NORMAL LOGIN (your existing logic – unchanged)
    if not identifier or not password:
        return Response(
            {"error": "Username/Phone and password are required"},
            status=400
        )

    # check by phone OR username
    user = User.objects.filter(phone=identifier).first() or \
           User.objects.filter(username=identifier).first()

    if not user:
        return Response({"error": "User not found"}, status=400)

    if not user.check_password(password):
        return Response({"error": "Invalid password"}, status=400)

    # generate JWT
    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Login successful",
        "user_type": "normal",
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }, status=200)
