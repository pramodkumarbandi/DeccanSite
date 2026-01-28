import razorpay
from django.conf import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

def create_contact(name, email):
    return client.contact.create({
        "name": name,
        "email": email,
        "type": "customer"
    })

def create_fund_account(contact_id, upi_id):
    return client.fund_account.create({
        "contact_id": contact_id,
        "account_type": "vpa",
        "vpa": {
            "address": upi_id
        }
    })

def create_payout(fund_account_id, amount):
    return client.payout.create({
        "account_number": "YOUR_RAZORPAY_ACCOUNT_NUMBER",
        "fund_account_id": fund_account_id,
        "amount": amount,
        "currency": "INR",
        "mode": "UPI",
        "purpose": "payout"
    })