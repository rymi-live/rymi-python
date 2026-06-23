from typing import Any, Dict
from rymi.client import RymiClient

class KeysResource:
    """Read-only access to publishable (browser-safe) keys.

    Creating or revoking keys mints/destroys credentials and changes standing
    config, so those remain dashboard actions and are not exposed here.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def list_publishable(self) -> Dict[str, Any]:
        """List publishable keys and their agent/channel scoping. Returns key prefixes only, never full secrets."""
        return self.client.get("/keys/publishable")
