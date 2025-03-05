from .client import APIBase


class Collect(APIBase):
    def checkout(self, email, amount, currency, **kwargs):
        """
        Generates payment checkout URL

        Args:
            email (string): Customer email
            amount (float): Total amount billed
            currency (string): Currency code (KES, USD, EUR, GBP)

        Returns:
            object: JSON dictionary with a checkout url field
        """
        method = kwargs.get("method")
        api_ref = kwargs.get("api_ref", "API Request")
        callback_url = kwargs.get("callback_url")
        redirect_url = kwargs.get("redirect_url")
        comment = kwargs.get("comment")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        phone_number = kwargs.get("phone_number")
        wallet_id = kwargs.get("wallet_id")
        mobile_tarrif = kwargs.get("mobile_tarrif", "BUSINESS-PAYS")
        card_tarrif = kwargs.get("card_tarrif", "BUSINESS-PAYS")
        payload = {
            "public_key": self.publishable_key,
            "currency": currency,
            "email": email,
            "amount": amount,
            "method": method,
            "api_ref": api_ref,
            "callback_url": callback_url,
            "redirect_url":redirect_url,
            "comment": comment,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "mobile_tarrif": mobile_tarrif,
            "card_tarrif": card_tarrif,
            "version": "3.0.0"
        }
        if wallet_id:
            payload.update({"wallet_id": wallet_id})
        return self.send_request("POST", "checkout/", payload, noauth=True)

    def status(self, invoice_id, checkout_id=None, signature=None):
        """
        Check status of transaction/invoice

        Args:
            invoice_id (string): Invoice or tracking ID
            checkout_id (string, optional): [Checkout id for payments requests through checkout API]. Defaults to None.
            signature (string, optional): [JWT signature for payments requests through checkout API]. Defaults to None.

        Returns:
            object: JSON with transaction details
        """
        payload = {
            "invoice_id": invoice_id,
            "public_key": self.publishable_key,
        }
        if checkout_id and signature:
            payload = {
                "invoice_id": invoice_id,
                "signature": signature,
                "checkout_id": checkout_id,
            }
        return self.send_request("POST", "payment/status/", payload, noauth=True)

    def mpesa_stk_push(self, phone_number, amount, narrative, currency="KES", api_ref="API Request", name=None, email=None, wallet_id=None):
        payload = {
            "public_key": self.publishable_key,
            "currency": currency,
            "method": "M-PESA",
            "amount": amount,
            "phone_number": phone_number,
            "api_ref": api_ref,
            "name": name,
            "email": email,
            "narrative": narrative
        }
        if wallet_id:
            payload.update({"wallet_id": wallet_id})
        return self.send_request("POST", "payment/mpesa-stk-push/", payload)

    def get_quote(self, amount, method, currency="KES", tarrif="BUSINESS-PAYS"):
        payload = {
            "public_key": self.publishable_key,
            "currency": currency,
            "method": method,
            "tarrif": tarrif,
            "amount": amount
        }
        return self.send_request("POST", "payment/get_amount_estimate/", payload)
