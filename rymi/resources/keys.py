from typing import Any, Dict, List, Optional
from rymi.client import RymiClient

class KeysResource:
    """Manage publishable (browser-safe) keys.

    These calls use your secret key, so run them server-side only. Publishable
    keys are scoped to a single agent and are safe to ship to the browser; the
    full key value is returned exactly once, at creation time.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def list_publishable(self) -> Dict[str, Any]:
        """List publishable keys and their agent/channel scoping. Returns key prefixes only, never full secrets."""
        return self.client.get("/keys/publishable")

    def create_publishable(
        self,
        agent_id: str,
        label: str,
        allowed_channels: Optional[List[str]] = None,
        audience: Optional[str] = None,
        default_from_number: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a publishable key scoped to an agent.

        The full ``key`` is only returned by this call — store it now, it is not
        retrievable later.
        """
        payload: Dict[str, Any] = {"agent_id": agent_id, "label": label}
        if allowed_channels is not None:
            payload["allowed_channels"] = allowed_channels
        if audience is not None:
            payload["audience"] = audience
        if default_from_number is not None:
            payload["default_from_number"] = default_from_number
        return self.client.post("/keys/publishable", json=payload)

    def revoke_publishable(self, key_id: str) -> Dict[str, Any]:
        """Revoke a publishable key by id."""
        return self.client.delete(f"/keys/publishable/{key_id}")
