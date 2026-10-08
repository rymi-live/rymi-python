from typing import Any, Dict, Optional
from rymi.client import RymiClient

# Tells "not passed" apart from None, which clears the operating country.
_UNSET: Any = object()


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

    def get_settings(self) -> Dict[str, Any]:
        """The workspace's compliance settings, with every country preset."""
        return self.client.get("/compliance/settings")

    def update_settings(self, operating_country: Any = _UNSET, rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Choosing ``operating_country`` fills every setting you haven't edited from its preset.
        ``operating_country=None`` clears the country and leaves the rules in place."""
        body: Dict[str, Any] = {}
        if operating_country is not _UNSET:
            body["operating_country"] = operating_country
        if rules is not None:
            body["rules"] = rules
        return self.client.put("/compliance/settings", json=body)

    def preview_settings(self, country: str) -> Dict[str, Any]:
        """What choosing a country would change, before saving."""
        return self.client.get("/compliance/settings/preview", params={"country": country})
