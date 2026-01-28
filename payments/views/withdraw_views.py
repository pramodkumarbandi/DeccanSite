from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payments.withdraw_services import create_contact, create_fund_account, create_payout
from payments.models import Withdrawal

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def withdraw_money(request):
    amount = int(request.data.get("amount")) * 100
    upi_id = request.data.get("upi_id")

    contact = create_contact(request.user.username, request.user.email)
    fund_account = create_fund_account(contact["id"], upi_id)
    payout = create_payout(fund_account["id"], amount)

    Withdrawal.objects.create(
        user=request.user,
        amount=amount,
        payout_id=payout["id"],
        status=payout["status"]
    )

    return Response({
        "status": "Withdrawal Initiated",
        "payout_id": payout["id"]
    })