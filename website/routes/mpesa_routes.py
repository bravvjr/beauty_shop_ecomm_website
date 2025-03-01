import base64
import datetime
import os
from requests.auth import HTTPBasicAuth
import requests

MPESA_AUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
MPESA_STK_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

def get_access_token():
    """Generate M-Pesa access token."""
    response = requests.get(
        MPESA_AUTH_URL, auth=HTTPBasicAuth(os.getenv("MPESA_CONSUMER_KEY"), os.getenv("MPESA_CONSUMER_SECRET"))
    )
    return response.json().get("access_token")

def stk_push(phone, amount, account_ref="OrderPayment"):
    """Initiate STK Push Payment"""
    access_token = get_access_token()
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{os.getenv('MPESA_SHORTCODE')}{os.getenv('MPESA_PASSKEY')}{timestamp}".encode()
    ).decode("utf-8")

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": os.getenv("MPESA_SHORTCODE"),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": os.getenv("MPESA_SHORTCODE"),
        "PhoneNumber": phone,
        "CallBackURL": os.getenv("MPESA_CALLBACK_URL"),
        "AccountReference": account_ref,
        "TransactionDesc": "Payment for goods",
    }

    try:
        response = requests.post(MPESA_STK_URL, json=payload, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error with STK Push: {e}")
        return {"error": str(e)}
