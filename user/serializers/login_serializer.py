from rest_framework import serializers
from user.models import User

# class LoginSerializer(serializers.Serializer):
#     login = serializers.CharField()  # username or phone
#     password = serializers.CharField()

#     def validate(self, data):
#         login = data.get('login')
#         password = data.get('password')

#         user = User.objects.filter(username=login).first() or \
#                User.objects.filter(phone=login).first()

#         if user and user.check_password(password):
        
#             raise serializers.ValidationError("Invalid Credentials")
#         return user



class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        login = data.get("login")
        password = data.get("password")

        user = User.objects.filter(username=login).first() or \
               User.objects.filter(phone=login).first()

        if not user:
            raise serializers.ValidationError("User not found")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid Credentials")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        # Return dictionary with actual user object
        data["user"] = user
        return data



