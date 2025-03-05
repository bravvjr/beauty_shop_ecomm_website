# from intasend import APIService

# # Initialize the IntaSend service
# publishable_key = "INTASEND_PUBLISHABLE_KEY"  # Replace with your key
# service = APIService(token=None, publishable_key=publishable_key, test=True)

# # Generate a checkout link
# response = service.collect.checkout(
#     phone_number="254712345678",  # Customer's phone number
#     email="john@doe.com",         # Customer's email
#     amount=10,                    # Amount to charge
#     currency="KES",               # Currency
#     comment="Service Fees",       # Optional comment
#     redirect_url="http://example.com/thank-you",  # Redirect URL
#     api_ref="order_12345",        # Optional reference for tracking
#     first_name="John",            # Optional first name
#     last_name="Doe",              # Optional last name
#     method="M-PESA"               # Optional payment method
# )




# from intasend import APIService

# API_PUBLISHABLE_KEY = 'ISPubKey_test_6fdcc500-15b3-476a-b5fc-9bc4f4523390'

# API_TOKEN = 'ISSecretKey_test_a99a507f-e552-497d-a4fb-5b6e13f4bf9d'

# service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)

# create_order = service.collect.mpesa_stk_push(phone_number='254799272949', amount=100, email='iamoragen@gmail.com', narrative='Payment for goods')

# print(create_order)

from intasend import APIService

API_PUBLISHABLE_KEY = 'ISPubKey_test_6fdcc500-15b3-476a-b5fc-9bc4f4523390'
API_TOKEN = 'ISSecretKey_test_a99a507f-e552-497d-a4fb-5b6e13f4bf9d'

service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)

try:
    response = service.collect.checkout(
        phone_number='254712345678',  # Replace with a valid phone number
        email='test@example.com',     # Replace with a valid email
        amount=10,                    # Total amount
        currency='KES',               # Currency
        comment='Test payment',       # Optional comment
        redirect_url='http://example.com/payment-successful',  # Replace with your redirect URL
        api_ref='test_order_123',     # Optional reference for tracking
    )
    print("Payment URL:", response.get('url'))
except Exception as e:
    print("Error:", str(e))