import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

def create_razorpay_order(amount):
    return client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

def verify_signature(data):
    client.utility.verify_payment_signature(data)