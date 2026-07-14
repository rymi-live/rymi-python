from typing import Any, Dict, List, Optional
from rymi.client import RymiClient


class CampaignMembersResource:
    """Manage a campaign's audience members."""

    def __init__(self, client: RymiClient):
        self.client = client

    def list(self, campaign_id: str, **params: Any) -> Dict[str, Any]:
        """List a campaign's members, paginated."""
        return self.client.get(f"/campaigns/{campaign_id}/members", params=params or None)

    def add(self, campaign_id: str, contact_ids: List[str], variables_override: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Attach existing contacts to a campaign as members."""
        payload: Dict[str, Any] = {"contact_ids": contact_ids}
        if variables_override is not None:
            payload["variables_override"] = variables_override
        return self.client.post(f"/campaigns/{campaign_id}/members", json=payload)

    def import_(
        self,
        campaign_id: str,
        contacts: Optional[List[Dict[str, Any]]] = None,
        csv: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Import inline contact rows (JSON or CSV): creates/merges contacts
        and attaches members in one call."""
        payload: Dict[str, Any] = {}
        if contacts is not None:
            payload["contacts"] = contacts
        if csv is not None:
            payload["csv"] = csv
        return self.client.post(f"/campaigns/{campaign_id}/members/import", json=payload)

    def update(self, campaign_id: str, member_id: str, **fields: Any) -> Dict[str, Any]:
        """Update a campaign member (status, variables, next attempt time)."""
        return self.client.patch(f"/campaigns/{campaign_id}/members/{member_id}", json=fields)

    def remove(self, campaign_id: str, member_id: str) -> Dict[str, Any]:
        """Remove a member from a campaign."""
        return self.client.delete(f"/campaigns/{campaign_id}/members/{member_id}")


class CampaignRoutesResource:
    """Manage a campaign's inbound routing rules."""

    def __init__(self, client: RymiClient):
        self.client = client

    def list(self, campaign_id: str, **params: Any) -> Dict[str, Any]:
        """List a campaign's inbound routing rules."""
        return self.client.get(f"/campaigns/{campaign_id}/routes", params=params or None)

    def create(self, campaign_id: str, phone_number: str, schedule: Optional[Dict[str, Any]] = None, active: Optional[bool] = None) -> Dict[str, Any]:
        """Bind an owned phone number to this campaign for inbound routing.

        Only one active route per number is allowed.
        """
        payload: Dict[str, Any] = {"phone_number": phone_number}
        if schedule is not None:
            payload["schedule"] = schedule
        if active is not None:
            payload["active"] = active
        return self.client.post(f"/campaigns/{campaign_id}/routes", json=payload)

    def update(self, campaign_id: str, route_id: str, **fields: Any) -> Dict[str, Any]:
        """Update an inbound route's schedule or active flag."""
        return self.client.patch(f"/campaigns/{campaign_id}/routes/{route_id}", json=fields)

    def remove(self, campaign_id: str, route_id: str) -> Dict[str, Any]:
        """Delete an inbound route."""
        return self.client.delete(f"/campaigns/{campaign_id}/routes/{route_id}")


class CampaignsResource:
    """Manage outbound/inbound calling campaigns."""

    def __init__(self, client: RymiClient):
        self.client = client
        self.members = CampaignMembersResource(client)
        self.routes = CampaignRoutesResource(client)

    def list(self, **params: Any) -> Dict[str, Any]:
        """List campaigns for the authenticated tenant, paginated."""
        return self.client.get("/campaigns", params=params or None)

    def create(
        self,
        agent_id: str,
        type: str,
        name: str,
        goal: Optional[Dict[str, Any]] = None,
        schedule_policy: Optional[Dict[str, Any]] = None,
        retry_policy: Optional[Dict[str, Any]] = None,
        concurrency_policy: Optional[Dict[str, Any]] = None,
        automation_policy: Optional[Dict[str, Any]] = None,
        reporting_policy: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new campaign in draft status against a published agent."""
        payload: Dict[str, Any] = {"agent_id": agent_id, "type": type, "name": name}
        if goal is not None:
            payload["goal"] = goal
        if schedule_policy is not None:
            payload["schedule_policy"] = schedule_policy
        if retry_policy is not None:
            payload["retry_policy"] = retry_policy
        if concurrency_policy is not None:
            payload["concurrency_policy"] = concurrency_policy
        if automation_policy is not None:
            payload["automation_policy"] = automation_policy
        if reporting_policy is not None:
            payload["reporting_policy"] = reporting_policy
        if metadata is not None:
            payload["metadata"] = metadata
        return self.client.post("/campaigns", json=payload)

    def retrieve(self, campaign_id: str) -> Dict[str, Any]:
        """Retrieve a single campaign by id."""
        return self.client.get(f"/campaigns/{campaign_id}")

    def update(self, campaign_id: str, **fields: Any) -> Dict[str, Any]:
        """Update campaign policy/goal fields.

        Status and lifecycle fields are not writable here.
        """
        return self.client.patch(f"/campaigns/{campaign_id}", json=fields)

    def launch(self, campaign_id: str) -> Dict[str, Any]:
        """Launch a campaign.

        Validates launch blockers, then stamps ``launched_at`` +
        ``agent_snapshot_id``, flips members to ``ready``, and transitions
        status to ``running``.
        """
        return self.client.post(f"/campaigns/{campaign_id}/launch")

    def launch_blockers(self, campaign_id: str) -> Dict[str, Any]:
        """Evaluate launch blockers without launching (dry run).

        Runs the same checks as :meth:`launch` but never transitions the
        campaign — safe to call from any status. Returns
        ``{"blockers": [...], "launchable": bool}``.
        """
        return self.client.get(f"/campaigns/{campaign_id}/launch-blockers")

    def pause(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a running campaign. In-flight calls finish naturally."""
        return self.client.post(f"/campaigns/{campaign_id}/pause")

    def resume(self, campaign_id: str) -> Dict[str, Any]:
        """Resume a paused campaign."""
        return self.client.post(f"/campaigns/{campaign_id}/resume")

    def archive(self, campaign_id: str) -> Dict[str, Any]:
        """Archive a campaign. Terminal — the scheduler never selects work for it again."""
        return self.client.post(f"/campaigns/{campaign_id}/archive")

    def report(self, campaign_id: str) -> Dict[str, Any]:
        """Read the campaign report: stat_* summary counters + outcome/sentiment/hourly/snapshot distributions."""
        return self.client.get(f"/campaigns/{campaign_id}/report")

    def attempts(self, campaign_id: str, **params: Any) -> Dict[str, Any]:
        """List a campaign's dial attempts, paginated."""
        return self.client.get(f"/campaigns/{campaign_id}/attempts", params=params or None)

    def batches(self, campaign_id: str, **params: Any) -> Dict[str, Any]:
        """List a campaign's sweep-claim batches, paginated."""
        return self.client.get(f"/campaigns/{campaign_id}/batches", params=params or None)

    def followups(self, campaign_id: str, **params: Any) -> Dict[str, Any]:
        """List a campaign's follow-up jobs, paginated."""
        return self.client.get(f"/campaigns/{campaign_id}/followups", params=params or None)

    def improve(self, campaign_id: str) -> Dict[str, Any]:
        """Run the improve engine: detectors gate an LLM proposal writer,
        persisting new campaign_suggestions."""
        return self.client.post(f"/campaigns/{campaign_id}/improve")

    def suggestions(self, campaign_id: str, **params: Any) -> Dict[str, Any]:
        """List a campaign's improvement suggestions, paginated."""
        return self.client.get(f"/campaigns/{campaign_id}/suggestions", params=params or None)

    def accept_suggestion(self, campaign_id: str, suggestion_id: str) -> Dict[str, Any]:
        """Accept a suggestion.

        Agent-editing suggestions create an agent-changes draft;
        campaign-policy suggestions patch the campaign.
        """
        return self.client.post(f"/campaigns/{campaign_id}/suggestions/{suggestion_id}/accept")

    def dismiss_suggestion(self, campaign_id: str, suggestion_id: str) -> Dict[str, Any]:
        """Dismiss a suggestion without applying it."""
        return self.client.post(f"/campaigns/{campaign_id}/suggestions/{suggestion_id}/dismiss")
