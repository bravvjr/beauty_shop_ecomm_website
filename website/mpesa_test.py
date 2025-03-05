from intasend import APIService

API_PUBLISHABLE_KEY = 'ISPubKey_live_1577ccf6-881c-4711-a6a5-f0699797b0e5'

API_TOKEN = 'ISSecretKey_live_82f96a3d-ae45-4c7d-b162-c3edb20f87c0'

service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)

create_order = service.collect.mpesa_stk_push(phone_number='254799272949', amount=100, email='iamoragen@gmail.com', narrative='Payment for goods')

print(create_order)