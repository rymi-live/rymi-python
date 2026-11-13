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

    def line(self) -> Dict[str, Any]:
        """Get the workspace's phone line from Rymi: status, KYC items still missing,
        call limits, and the release date when rental is unpaid."""
        return self.client.get("/telephony/line")

    def request_line(self, country: str, handoff: Optional[str] = None) -> Dict[str, Any]:
        """Start or resume a phone line from Rymi for ``"IN"`` or ``"US"``.

        ``handoff`` is ``"studio"`` (default), ``"whatsapp"`` or ``"both"``. Returns the
        Studio onboarding URL in ``studio_url``.
        """
        payload: Dict[str, Any] = {"country": country}
        if handoff is not None:
            payload["handoff"] = handoff
        return self.client.post("/telephony/line/request", json=payload)

    def accept_line_terms(self) -> Dict[str, Any]:
        """Accept the current phone line terms for the workspace's line."""
        return self.client.post("/telephony/line/accept-terms", json={})

    def submit_line_kyc(
        self,
        fields: Optional[Dict[str, str]] = None,
        document: Optional[Dict[str, str]] = None,
        submit: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update India KYC for the line, optionally upload one document and submit.

        ``document`` is ``{"filename", "mime_type", "content_base64"}`` (PDF, JPEG or
        PNG). With ``submit=True`` Rymi files the application once nothing is missing.
        """
        payload: Dict[str, Any] = {}
        if fields is not None:
            payload["fields"] = fields
        if document is not None:
            payload["document"] = document
        if submit is not None:
            payload["submit"] = submit
        return self.client.post("/telephony/line/kyc", json=payload)
