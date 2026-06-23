from typing import Optional
from .client import RymiClient, RymiError
from .resources.agents import AgentsResource
from .resources.calls import CallsResource
from .resources.numbers import NumbersResource
from .resources.telephony import TelephonyResource
from .resources.keys import KeysResource
from .resources.billing import BillingResource
from .resources.templates import TemplatesResource
from .resources.webhooks import WebhooksUtility

class Rymi:
    """The official Python SDK for the Rymi Voice API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self._client = RymiClient(api_key=api_key, base_url=base_url)

        self.agents = AgentsResource(self._client)
        self.calls = CallsResource(self._client)
        self.numbers = NumbersResource(self._client)
        self.telephony = TelephonyResource(self._client)
        self.keys = KeysResource(self._client)
        self.billing = BillingResource(self._client)
        self.templates = TemplatesResource(self._client)
        self.webhooks = WebhooksUtility()

__all__ = ["Rymi", "RymiError"]
