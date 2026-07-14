from typing import Any, Dict, List, Optional
from rymi.client import RymiClient


class ContactsResource:
    """Manage tenant-level contacts used as campaign audience members."""

    def __init__(self, client: RymiClient):
        self.client = client

    def list(self, **params: Any) -> Dict[str, Any]:
        """List tenant-level contacts, paginated."""
        return self.client.get("/contacts", params=params or None)

    def create(
        self,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        timezone: Optional[str] = None,
        language: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        consent: Optional[Dict[str, bool]] = None,
        source: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a tenant-level contact.

        If a contact with the same (tenant, phone) already exists, the
        existing row is returned instead of creating a duplicate — check
        ``deduped`` in the response.
        """
        payload: Dict[str, Any] = {}
        if phone is not None:
            payload["phone"] = phone
        if email is not None:
            payload["email"] = email
        if name is not None:
            payload["name"] = name
        if timezone is not None:
            payload["timezone"] = timezone
        if language is not None:
            payload["language"] = language
        if tags is not None:
            payload["tags"] = tags
        if custom_fields is not None:
            payload["custom_fields"] = custom_fields
        if consent is not None:
            payload["consent"] = consent
        if source is not None:
            payload["source"] = source
        return self.client.post("/contacts", json=payload)

    def retrieve(self, contact_id: str) -> Dict[str, Any]:
        """Retrieve a single tenant-scoped contact by id."""
        return self.client.get(f"/contacts/{contact_id}")

    def update(self, contact_id: str, **fields: Any) -> Dict[str, Any]:
        """Update an existing tenant-scoped contact. Only provided fields change."""
        return self.client.patch(f"/contacts/{contact_id}", json=fields)

    def delete(self, contact_id: str) -> Dict[str, Any]:
        """Delete a tenant-scoped contact."""
        return self.client.delete(f"/contacts/{contact_id}")

    def import_(
        self,
        contacts: Optional[List[Dict[str, Any]]] = None,
        csv: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Bulk import contacts from JSON rows or CSV text.

        Each row's phone is normalized to E.164 and upserted on
        (tenant_id, phone); rows with unparseable phones are skipped and
        reported in ``invalid``.
        """
        payload: Dict[str, Any] = {}
        if contacts is not None:
            payload["contacts"] = contacts
        if csv is not None:
            payload["csv"] = csv
        return self.client.post("/contacts/import", json=payload)

    def set_consent(
        self,
        contact_id: str,
        channel: str,
        granted: bool,
        source: Optional[str] = None,
        method: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Record a consent grant or revoke for one channel, with evidence.

        Also appends an immutable row to the consent_events proof log.
        """
        payload: Dict[str, Any] = {"channel": channel, "granted": granted}
        if source is not None:
            payload["source"] = source
        if method is not None:
            payload["method"] = method
        return self.client.patch(f"/contacts/{contact_id}/consent", json=payload)
