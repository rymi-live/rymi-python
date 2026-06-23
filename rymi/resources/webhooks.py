import hmac
import hashlib
import time
from typing import Any, Dict, List, Optional
from rymi.client import RymiClient

class WebhooksResource:
    """Manage webhook endpoints and verify incoming webhook signatures.

    The CRUD methods register/maintain the endpoints Rymi delivers events to.
    ``verify_signature`` is a stateless helper for authenticating deliveries on
    your backend and can be called without an API key.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def list(self, **params: Any) -> Dict[str, Any]:
        """List registered webhook endpoints."""
        return self.client.get("/webhooks", params=params or None)

    def create(
        self,
        url: str,
        events: List[str],
        secret: str,
        alert_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Register a webhook endpoint. Keep ``secret`` to verify deliveries."""
        payload: Dict[str, Any] = {"url": url, "events": events, "secret": secret}
        if alert_email is not None:
            payload["alert_email"] = alert_email
        return self.client.post("/webhooks", json=payload)

    def update(
        self,
        webhook_id: str,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        secret: Optional[str] = None,
        alert_email: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an endpoint's URL, events, secret, or alert email."""
        payload: Dict[str, Any] = {}
        if url is not None:
            payload["url"] = url
        if events is not None:
            payload["events"] = events
        if secret is not None:
            payload["secret"] = secret
        if alert_email is not None:
            payload["alert_email"] = alert_email
        return self.client.patch(f"/webhooks/{webhook_id}", json=payload)

    def delete(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook endpoint."""
        return self.client.delete(f"/webhooks/{webhook_id}")

    @staticmethod
    def verify_signature(
        payload: str,
        signature_header: str,
        timestamp_header: str,
        webhook_secret: str,
        tolerance_millis: int = 300000  # 5 minutes
    ) -> bool:
        """
        Verifies that a webhook received by your backend was genuinely dispatched by Rymi.

        Rymi endpoints secure webhooks by computing an HMAC-SHA256 signature
        of the raw JSON body concatenated with the timestamp using your Webhook Secret.
        """
        # 1. Check for Replay Attacks
        try:
            timestamp = int(timestamp_header)
        except ValueError:
            raise ValueError("Invalid Rymi-Timestamp header format.")

        current_time = int(time.time() * 1000)
        if (current_time - timestamp) > tolerance_millis:
            raise ValueError("Webhook timestamp is too old. Possible replay attack.")

        # 2. Prepare the verification string
        signature_payload = f"{timestamp}.{payload}"

        # 3. Compute expected HMAC
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            signature_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # 4. Secure string comparison
        if not hmac.compare_digest(signature_header, expected_signature):
            raise ValueError("Invalid Webhook Signature. The secret might be incorrect.")

        return True


# Backwards-compatible alias for the pre-CRUD utility class.
WebhooksUtility = WebhooksResource
