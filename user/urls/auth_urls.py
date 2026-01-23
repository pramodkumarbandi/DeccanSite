from django.urls import path
from user.views.auth_views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view()),
]