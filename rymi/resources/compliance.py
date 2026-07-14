from typing import Any, Dict, Optional
from rymi.client import RymiClient


class ComplianceResource:
    """Record and list compliance attestations (append-only)."""

    def __init__(self, client: RymiClient):
        self.client = client

    def attest(self, kind: str, note: Optional[str] = None) -> Dict[str, Any]:
        """Record a compliance attestation.

        Campaign launch blockers in "attested" mode read the most recent
        attestation of the matching ``kind`` (``dnc_external_scrub`` or
        ``ai_disclosure``).
        """
        payload: Dict[str, Any] = {"kind": kind}
        if note is not None:
            payload["note"] = note
        return self.client.post("/compliance/attestations", json=payload)

    def list_attestations(self) -> Dict[str, Any]:
        """List the tenant's 50 most recent compliance attestations, newest first."""
        return self.client.get("/compliance/attestations")
