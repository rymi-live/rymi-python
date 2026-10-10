from typing import Any, Dict
from urllib.parse import quote

from rymi.client import RymiClient


class AccountsResource:
    """Accounts you belong to, their members, and the workspaces in each."""

    def __init__(self, client: RymiClient):
        self.client = client

    def list(self) -> Dict[str, Any]:
        return self.client.get("/accounts")

    def get(self, account_id: str) -> Dict[str, Any]:
        return self.client.get(f"/accounts/{quote(account_id, safe='')}")

    def update(self, account_id: str, name: str) -> Dict[str, Any]:
        return self.client.patch(f"/accounts/{quote(account_id, safe='')}", json={"name": name})

    def list_members(self, account_id: str) -> Dict[str, Any]:
        return self.client.get(f"/accounts/{quote(account_id, safe='')}/members")

    def add_member(self, account_id: str, email: str, role: str) -> Dict[str, Any]:
        """``role`` is owner, admin, or billing."""
        return self.client.post(
            f"/accounts/{quote(account_id, safe='')}/members",
            json={"email": email, "role": role},
        )

    def update_member(self, account_id: str, user_id: str, role: str) -> Dict[str, Any]:
        """Returns ``{"member": {"user_id", "role"}}`` (no email)."""
        return self.client.patch(
            f"/accounts/{quote(account_id, safe='')}/members/{quote(user_id, safe='')}",
            json={"role": role},
        )

    def remove_member(self, account_id: str, user_id: str) -> Dict[str, Any]:
        return self.client.delete(
            f"/accounts/{quote(account_id, safe='')}/members/{quote(user_id, safe='')}"
        )

    def workspaces(self, account_id: str) -> Dict[str, Any]:
        """Workspaces in the account, with this month's calls, minutes, and credits."""
        return self.client.get(f"/accounts/{quote(account_id, safe='')}/workspaces")
