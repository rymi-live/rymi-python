from typing import Any, Dict, List, Optional
from rymi.client import RymiClient

class DncResource:
    """Do-Not-Call registry.

    Numbers are normalized to E.164 server-side on both read and write, so any
    input format is accepted. Outbound calls to blocked numbers are refused.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def list(self, **params: Any) -> Dict[str, Any]:
        """List all DNC entries for the tenant."""
        return self.client.get("/dnc", params=params or None)

    def add(self, phone_number: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Add a single number to the Do-Not-Call registry."""
        payload: Dict[str, Any] = {"phone_number": phone_number}
        if reason is not None:
            payload["reason"] = reason
        return self.client.post("/dnc", json=payload)

    def add_batch(self, phone_numbers: List[str], reason: Optional[str] = None) -> Dict[str, Any]:
        """Add up to 1000 numbers in one request. Invalid numbers are skipped and returned in ``invalid``."""
        payload: Dict[str, Any] = {"phone_numbers": phone_numbers}
        if reason is not None:
            payload["reason"] = reason
        return self.client.post("/dnc/batch", json=payload)

    def check(self, phone_numbers: List[str]) -> Dict[str, Any]:
        """Check up to 500 numbers without adding them. Read-only."""
        return self.client.post("/dnc/check", json={"phone_numbers": phone_numbers})

    def remove(self, phone: str) -> Dict[str, Any]:
        """Remove a number from the registry (re-enables outbound to it)."""
        return self.client.delete(f"/dnc/{phone}")
