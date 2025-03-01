import base64
import requests

def get_access_token():
    # Safaricom's API URL
    url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    api_key = 'HBhZnGuONYvCdEYxCRvZJWDYotDSG1yESPB4WlhMCEhh67y6'  
    api_secret = 'jCBMHRqA3cvZkMIkmxAftDcGzMEz3dJAiJI3nM1SYUoJJwRunwmKuCCRZGBeymst'  
    
    # Basic Authentication (base64 encoded)
    auth = base64.b64encode(f'{api_key}:{api_secret}'.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {auth}'}

    # Send request to get the access token
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Extract access token from the response
        json_response = response.json()
        return json_response['access_token']
    else:
        return None  

def lipa_na_mpesa(phone_number, amount):
    headers = {
        'Authorization': f'Bearer {get_access_token()}',
        'Content-Type': 'application/json'
    }

    payload = {
        "BusinessShortcode": "174379", 
        "LipaNaMpesaOnlineShortcode": "174379",  
        "LipaNaMpesaOnlineShortcodePassword": "YourLipaShortcodePassword", 
        "PhoneNumber": phone_number,
        "Amount": amount,
        "AccountReference": "AccountRef123",  # The reference for your transaction
        "TransactionDesc": "Payment for order",
        "CallBackURL": "https://yourdomain.com/mpesa/callback", 
        "TransactionType": "Payment"  
    }

    # Safaricom STK Push endpoint
    stk_push_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
    # Send request to the Safaricom API
    response = requests.post(stk_push_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        json_response = response.json()
        return json_response  # Contains information about the payment status
    else:
        return response.json()  # Handle the failure case
