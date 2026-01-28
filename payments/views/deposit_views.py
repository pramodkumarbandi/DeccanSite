from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payments.models import Payment
from payments.deposit_services import create_razorpay_order, verify_signature

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deposit_money(request):
    amount = int(request.data.get("amount")) * 100

    order = create_razorpay_order(amount)

    Payment.objects.create(
        user=request.user,
        order_id=order["id"],
        amount=amount,
        status="created"
    )

    return Response(order)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_deposit(request):
    data = request.data
    try:
        verify_signature(data)

        Payment.objects.filter(order_id=data["razorpay_order_id"]).update(
            payment_id=data["razorpay_payment_id"],
            status="success"
        )

        return Response({"status": "Deposit Successful"})
    except:
        return Response({"status": "Deposit Failed"}, status=400)