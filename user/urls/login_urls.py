from django.urls import path
from ..views.login_views import login
from ..views.logout_views import logout

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
