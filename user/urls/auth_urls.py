from django.urls import path
from user.views.auth_views import LoginView, SignupView, SendOTPView, VerifyOTPView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('signup/', SignupView.as_view()),
]
