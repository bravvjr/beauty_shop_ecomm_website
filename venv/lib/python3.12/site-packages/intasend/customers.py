from .client import APIBase


class Customers(APIBase):
    def details(self, customer_id):
        return self.send_request("GET", f"customers/{customer_id}", None)

    def create(self, email, **kwargs):
        payload = kwargs
        payload["email"] = email
        return self.send_request("POST", "customers/", payload)

    def retrieve(self, customer_id=None):
        if customer_id:
            return self.details(customer_id)
        return self.send_request("GET", "customers/", None)

    def transactions(self, customer_id):
        return self.send_request("GET", f"customers/{customer_id}/transactions", None)
