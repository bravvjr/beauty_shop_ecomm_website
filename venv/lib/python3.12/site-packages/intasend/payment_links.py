from .client import APIBase


class PaymentLinks(APIBase):
    def details(self, link_id):
        return self.send_request("GET", f"paymentlinks/{link_id}", None)

    def create(self, title, currency, amount=0, mobile_tarrif="BUSINESS-PAYS", card_tarrif="BUSINESS-PAYS", is_active=True, **kwargs):
        payload = kwargs
        payload["title"] = title
        payload["currency"] = currency
        payload["amount"] = amount
        payload["mobile_tarrif"] = mobile_tarrif
        payload["card_tarrif"] = card_tarrif
        payload["is_active"] = is_active
        return self.send_request("POST", "paymentlinks/", payload)

    def retrieve(self, link_id=None):
        if link_id:
            return self.details(link_id)
        return self.send_request("GET", "paymentlinks/", None)

    def deactivate(self):
        return self.send_request("GET", "paymentlinks/", None)

    def update(self):
        return self.send_request("GET", "paymentlinks/", None)
