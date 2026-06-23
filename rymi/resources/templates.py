from typing import Any, Dict
from rymi.client import RymiClient

class TemplatesResource:
    """Published agent templates."""

    def __init__(self, client: RymiClient):
        self.client = client

    def list(self) -> Dict[str, Any]:
        """List published agent templates. Use a template's `defaults` as the starting config for agents.create()."""
        return self.client.get("/agent-templates")
