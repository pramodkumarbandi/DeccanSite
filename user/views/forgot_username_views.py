from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.models import User
from user.utils import validate_phone


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_username(request):
    phone = request.data.get('phone')

    is_valid, msg = validate_phone(phone)
    if not is_valid:
        return Response({"error": msg}, status=400)

    try:
        user = User.objects.get(phone=phone)
        return Response({
            "message": "Username found successfully",
            "username": user.username
        })
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
