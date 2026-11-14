from typing import Any, Dict, Optional
from rymi.client import RymiClient


class BugReportsResource:
    """Bug reports.

    A report is queued as ``pending_review``; Rymi reviews every report before
    work starts. ``status`` then moves to ``approved``, ``in_progress`` and
    ``fixed`` (with ``fix_ref``), or to ``rejected`` / ``duplicate``.
    """

    def __init__(self, client: RymiClient):
        self.client = client

    def create(
        self,
        title: str,
        description: str,
        *,
        steps: Optional[str] = None,
        expected: Optional[str] = None,
        actual: Optional[str] = None,
        severity: Optional[str] = None,
        area: Optional[str] = None,
        call_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        source: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Report a bug. ``severity``: low, medium (default), high, critical."""
        payload: Dict[str, Any] = {"title": title, "description": description}
        for key, value in (
            ("steps", steps), ("expected", expected), ("actual", actual), ("severity", severity),
            ("area", area), ("call_id", call_id), ("agent_id", agent_id), ("source", source),
        ):
            if value is not None:
                payload[key] = value
        return self.client.post("/bug-reports", json=payload)

    def list(self, **params: Any) -> Dict[str, Any]:
        """List this workspace's bug reports, newest first. Accepts ``limit``, ``offset`` and ``status``."""
        return self.client.get("/bug-reports", params=params or None)

    def retrieve(self, bug_report_id: str) -> Dict[str, Any]:
        """One bug report, with its review status."""
        return self.client.get(f"/bug-reports/{bug_report_id}")
