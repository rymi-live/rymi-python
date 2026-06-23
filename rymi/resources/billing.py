from typing import Any, Dict, List, Optional
from rymi.client import RymiClient

class BillingResource:
    """Account usage and spend controls.

    Voice balance is reported in MINUTES, not dollars. The spend-control methods
    (auto-recharge, alerts, estimate) are denominated in USD because they manage
    money, not balance display.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def usage_summary(self) -> Dict[str, Any]:
        """Lane-aware usage summary: remaining voice-runtime minutes, Studio AI unit
        usage, and post-call intelligence usage."""
        return self.client.get("/billing/usage-summary")

    def estimate(
        self,
        tier: Optional[str] = None,
        duration_seconds: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Estimate a call's cost for a role tier and duration before dialing."""
        payload: Dict[str, Any] = {}
        if tier is not None:
            payload["tier"] = tier
        if duration_seconds is not None:
            payload["duration_seconds"] = duration_seconds
        return self.client.post("/billing/estimate", json=payload)

    def set_auto_recharge(
        self,
        enabled: Optional[bool] = None,
        pack_usd: Optional[float] = None,
        threshold_usd: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Configure automatic balance top-ups (USD)."""
        payload: Dict[str, Any] = {}
        if enabled is not None:
            payload["enabled"] = enabled
        if pack_usd is not None:
            payload["pack_usd"] = pack_usd
        if threshold_usd is not None:
            payload["threshold_usd"] = threshold_usd
        return self.client.put("/billing/auto-recharge", json=payload)

    def set_alerts(
        self,
        thresholds_usd: Optional[List[float]] = None,
        low_balance_pct: Optional[float] = None,
        email_enabled: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Configure spend-threshold and low-balance alerts (USD)."""
        payload: Dict[str, Any] = {}
        if thresholds_usd is not None:
            payload["thresholds_usd"] = thresholds_usd
        if low_balance_pct is not None:
            payload["low_balance_pct"] = low_balance_pct
        if email_enabled is not None:
            payload["email_enabled"] = email_enabled
        return self.client.put("/billing/alerts", json=payload)
