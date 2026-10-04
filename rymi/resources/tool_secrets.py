from typing import Any, Dict
from urllib.parse import quote
from rymi.client import RymiClient


class ToolSecretsResource:
    """Workspace secrets for API-tool headers, referenced as ``{{secrets.NAME}}``.

    Each secret is pinned to one host and only sent to it. Values are write-only.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def list(self) -> Dict[str, Any]:
        """Secret names and the host each is pinned to (never the values)."""
        return self.client.get("/tool-secrets")

    def set(self, name: str, value: str, host: str) -> Dict[str, Any]:
        """Create or replace a secret. ``name`` is UPPER_SNAKE_CASE; ``host`` is a public hostname."""
        return self.client.put(f"/tool-secrets/{quote(name, safe='')}", json={"value": value, "host": host})

    def delete(self, name: str) -> Dict[str, Any]:
        """Delete a secret."""
        return self.client.delete(f"/tool-secrets/{quote(name, safe='')}")
