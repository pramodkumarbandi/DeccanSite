from django.urls import path
from user.views.forgot_username_views import forgot_username
from user.views.forgot_password_views import send_otp, reset_password

urlpatterns = [
    path('forgot-username/', forgot_username),
    path('send-otp/', send_otp),
    path('reset-password/', reset_password),
]
