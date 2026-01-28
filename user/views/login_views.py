from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    identifier = request.data.get("identifier")  # username or phone
    password = request.data.get("password")

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
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }, status=200)
