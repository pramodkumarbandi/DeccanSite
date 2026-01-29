from django.urls import path
from ..views.auth_views import send_otp, verify_otp, register

urlpatterns = [
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('register/', register, name='register'),
]
