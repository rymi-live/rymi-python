from typing import Any, Dict
from rymi.client import RymiClient


class PhoneConfirmationResource:
    """Message-only confirmation for a shared-test-line destination.

    ``start`` does not confirm the number. The phone confirms it by sending
    ``message_text`` to Rymi on WhatsApp. ``status`` only reads that result.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def start(self, phone: str) -> Dict[str, Any]:
        """Open a confirmation request for ``phone``, or report that it is already confirmed."""
        return self.client.post("/phone-confirmation/start", json={"phone": phone})

    def status(self, phone: str) -> Dict[str, Any]:
        """Whether this account has confirmed ``phone`` for shared test lines."""
        return self.client.get("/phone-confirmation/status", params={"phone": phone})
