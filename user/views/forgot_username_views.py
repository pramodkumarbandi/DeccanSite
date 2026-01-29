from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from user.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_username(request):
    phone = request.data.get('phone')

    if not phone:
        return Response({"error": "Phone number is required"}, status=400)

    try:
        user = User.objects.get(phone=phone)
        return Response({
            "message": "Username found successfully",
            "username": user.username
        })
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
