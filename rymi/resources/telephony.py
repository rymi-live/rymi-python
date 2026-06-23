from typing import Any, Dict
from rymi.client import RymiClient

class TelephonyResource:
    """Inspect the connected telephony carrier.

    Connecting/disconnecting a carrier requires carrier credentials and changes a
    standing integration, so it is a dashboard action and not exposed here.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def status(self) -> Dict[str, Any]:
        """Report whether a carrier is connected, and which provider/account."""
        return self.client.get("/telephony/status")

    def numbers(self) -> Dict[str, Any]:
        """List numbers available on the connected telephony carrier account."""
        return self.client.get("/telephony/numbers")
