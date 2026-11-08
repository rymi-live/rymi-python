from typing import Any, Dict
from rymi.client import RymiClient


class PhoneConfirmationResource:
    """Confirm a shared-test-line destination.

    This never touches login. A confirmed number only lets Rymi's test lines
    ring it, and it is not consent to future calls.

    ``start`` returns a WhatsApp link: the phone confirms by sending
    ``message_text``. ``request_code`` sends a code to the phone: a person types
    it at ``entry_url`` while signed in to Studio. No secret key can submit a code.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def start(self, phone: str) -> Dict[str, Any]:
        """Open a WhatsApp confirmation for ``phone``, or report that it is already confirmed."""
        return self.client.post("/phone-confirmation/start", json={"phone": phone})

    def request_code(self, phone: str) -> Dict[str, Any]:
        """Send a code to ``phone`` on WhatsApp. The code is never returned."""
        return self.client.post("/phone-confirmation/request-code", json={"phone": phone})

    def status(self, phone: str) -> Dict[str, Any]:
        """Whether this account has confirmed ``phone``, and any code still waiting to be entered."""
        return self.client.get("/phone-confirmation/status", params={"phone": phone})
