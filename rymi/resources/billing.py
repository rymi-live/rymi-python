from typing import Any, Dict
from rymi.client import RymiClient

class BillingResource:
    """Account usage. Voice balance is reported in MINUTES, not dollars."""

    def __init__(self, client: RymiClient):
        self.client = client

    def usage_summary(self) -> Dict[str, Any]:
        """Lane-aware usage summary: remaining voice-runtime minutes, Studio AI unit
        usage, and post-call intelligence usage."""
        return self.client.get("/billing/usage-summary")
