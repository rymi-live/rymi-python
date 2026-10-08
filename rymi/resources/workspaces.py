from typing import Any, Dict, Optional
from urllib.parse import quote

from rymi.client import RymiClient


class WorkspacesResource:
    """Workspaces you can act in, client workspaces your agency pays for, their usage and members."""

    def __init__(self, client: RymiClient):
        self.client = client

    def list(self) -> Dict[str, Any]:
        return self.client.get("/workspaces")

    def create(self, name: str, operating_country: Optional[str] = None, parent: Optional[str] = None) -> Dict[str, Any]:
        """``parent``: an agency workspace you run; the new workspace becomes its client and the agency pays its calls."""
        body: Dict[str, Any] = {"name": name}
        if operating_country is not None:
            body["operating_country"] = operating_country
        if parent is not None:
            body["parent"] = parent
        return self.client.post("/workspaces", json=body)

    def update(self, workspace_id: str, **fields: Any) -> Dict[str, Any]:
        """Fields: ``name``, ``operating_country``, ``spend_cap_cents_monthly`` (client workspaces; None removes the cap)."""
        return self.client.patch(f"/workspaces/{quote(workspace_id, safe='')}", json=fields)

    def delete(self, workspace_id: str) -> Dict[str, Any]:
        """Delete an empty workspace (no agents, numbers, calls, campaigns or client workspaces). Owner only; never your first workspace."""
        return self.client.delete(f"/workspaces/{quote(workspace_id, safe='')}")

    def usage(self, workspace_id: str, month: Optional[str] = None) -> Dict[str, Any]:
        """Calls, minutes and credits for a month (YYYY-MM, UTC; default this month)."""
        params = {"month": month} if month else None
        return self.client.get(f"/workspaces/{quote(workspace_id, safe='')}/usage", params=params)

    def list_members(self, workspace_id: str) -> Dict[str, Any]:
        return self.client.get(f"/workspaces/{quote(workspace_id, safe='')}/members")

    def add_member(self, workspace_id: str, email: str, role: Optional[str] = None) -> Dict[str, Any]:
        """Someone without a Rymi account gets an invite email. Client workspaces take the client role."""
        body: Dict[str, Any] = {"email": email}
        if role is not None:
            body["role"] = role
        return self.client.post(f"/workspaces/{quote(workspace_id, safe='')}/members", json=body)

    def remove_member(self, workspace_id: str, user_id: str) -> Dict[str, Any]:
        return self.client.delete(f"/workspaces/{quote(workspace_id, safe='')}/members/{quote(user_id, safe='')}")
