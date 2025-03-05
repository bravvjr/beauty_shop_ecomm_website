import requests

from .exceptions import (IntaSendBadRequest, IntaSendNotAllowed,
                         IntaSendServerError, IntaSendUnauthorized)


def get_service_url(service_endpoint, test=False):
    if test:
        return f"https://sandbox.intasend.com/api/v1/{service_endpoint}"
    return f"https://payment.intasend.com/api/v1/{service_endpoint}"


class APIBase(object):
    def __init__(self, **kwargs):
        """API helper defination."""
        self.token = kwargs.get("token")
        self.publishable_key = kwargs.get("publishable_key")
        self.test = kwargs.get("test", False)
        if not self.token:
            raise Exception("Authentication token is required")
        super().__init__()

    def send_request(self, request_type, service_endpoint, payload, noauth=False):
        url = get_service_url(service_endpoint,  self.test)
        headers = self.get_headers(noauth)
        
        resp = requests.request(
            request_type, url, json=payload, headers=headers)
        if resp.status_code == 400:
            raise IntaSendBadRequest(resp.text)
        elif resp.status_code == 403:
            raise IntaSendNotAllowed(resp.text)
        elif resp.status_code == 500:
            raise IntaSendServerError(resp.text)
        elif resp.status_code == 401:
            raise IntaSendUnauthorized(resp.text)
        return resp.json()

    def get_headers(self, noauth=False):
        if noauth:
            return {"INTASEND_PUBLIC_API_KEY": self.publishable_key}
        return {
            "Authorization": f"Bearer {self.token}",
            "INTASEND_PUBLIC_API_KEY": self.publishable_key
        }
