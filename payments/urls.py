from django.urls import path
from payments.views.deposit_views import deposit_money, verify_deposit
from payments.views.withdraw_views import withdraw_money

urlpatterns = [
    path("deposit/", deposit_money),
    path("verify/", verify_deposit),
    path("withdraw/", withdraw_money),
]