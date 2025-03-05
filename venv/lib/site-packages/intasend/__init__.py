"""IntaSend Payments API for Python 3."""
from .collections import Collect
from .transfers import Transfer
from .wallets import Wallet
from .chargebacks import Chagebacks
from .payment_links import PaymentLinks
from .customers import Customers


class APIService:
    def __init__(self, **kwargs):
        """API Services Initialization."""
        self.collect = Collect(**kwargs)
        self.transfer = Transfer(**kwargs)
        self.wallets = Wallet(**kwargs)
        self.chargebacks = Chagebacks(**kwargs)
        self.customers = Customers(**kwargs)
        self.payment_links = PaymentLinks(**kwargs)
