from typing import Any, Dict, Optional
from rymi.client import RymiClient

class TelephonyResource:
    """Inspect and manage the connected telephony carrier.

    Most teams connect a carrier once from the dashboard; ``connect`` /
    ``disconnect`` exist for programmatic provisioning and require carrier
    credentials.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def status(self) -> Dict[str, Any]:
        """Report whether a carrier is connected, and which provider/account."""
        return self.client.get("/telephony/status")

    def numbers(self) -> Dict[str, Any]:
        """List numbers available on the connected telephony carrier account."""
        return self.client.get("/telephony/numbers")

    def connect(
        self,
        provider: str,
        auth_id: Optional[str] = None,
        auth_token: Optional[str] = None,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        signature_secret: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Connect a telephony carrier. Requires that carrier's credentials."""
        payload: Dict[str, Any] = {"provider": provider}
        for key, value in (
            ("auth_id", auth_id),
            ("auth_token", auth_token),
            ("api_key", api_key),
            ("api_secret", api_secret),
            ("signature_secret", signature_secret),
        ):
            if value is not None:
                payload[key] = value
        return self.client.post("/telephony/connect", json=payload)

    def disconnect(self) -> Dict[str, Any]:
        """Disconnect the currently connected carrier."""
        return self.client.post("/telephony/disconnect")
