# packages/python/tests/test_workspaces.py
import json
import os

import pytest
import responses

from rymi import Rymi

API = "https://api.rymi.live/v1"


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("RYMI_API_KEY", "rymi_test_123")
    monkeypatch.delenv("RYMI_WORKSPACE", raising=False)


@responses.activate
def test_workspace_header_option_env_and_with_workspace(monkeypatch):
    responses.add(responses.GET, f"{API}/agents", json={"agents": []})
    Rymi(workspace="w2").agents.list()
    assert responses.calls[0].request.headers["Rymi-Workspace"] == "w2"

    Rymi().agents.list()
    assert "Rymi-Workspace" not in responses.calls[1].request.headers

    monkeypatch.setenv("RYMI_WORKSPACE", "w3")
    rymi = Rymi()
    rymi.agents.list()
    assert responses.calls[2].request.headers["Rymi-Workspace"] == "w3"

    rymi.with_workspace("c1").agents.list()
    assert responses.calls[3].request.headers["Rymi-Workspace"] == "c1"
    assert responses.calls[3].request.headers["Authorization"] == "Bearer rymi_test_123"


@responses.activate
def test_workspaces_resource():
    responses.add(responses.GET, f"{API}/workspaces", json={"workspaces": []})
    responses.add(responses.POST, f"{API}/workspaces", json={"workspace": {"id": "c1"}}, status=201)
    responses.add(responses.PATCH, f"{API}/workspaces/c1", json={"ok": True})
    responses.add(responses.GET, f"{API}/workspaces/c1/usage", json={"calls": 1})
    responses.add(responses.GET, f"{API}/workspaces/c1/members", json={"members": []})
    responses.add(responses.POST, f"{API}/workspaces/c1/members", json={"member": {}}, status=201)
    responses.add(responses.DELETE, f"{API}/workspaces/c1/members/u2", json={"ok": True})
    responses.add(responses.DELETE, f"{API}/workspaces/c1", json={"ok": True})

    rymi = Rymi()
    rymi.workspaces.list()
    rymi.workspaces.create("Sarang", parent="agency-1")
    rymi.workspaces.update("c1", spend_cap_cents_monthly=2000)
    rymi.workspaces.usage("c1", month="2026-10")
    rymi.workspaces.list_members("c1")
    rymi.workspaces.add_member("c1", "guest@example.com")
    rymi.workspaces.remove_member("c1", "u2")
    rymi.workspaces.delete("c1")

    sent = [(c.request.method, c.request.url, json.loads(c.request.body) if c.request.body else None) for c in responses.calls]
    assert sent == [
        ("GET", f"{API}/workspaces", None),
        ("POST", f"{API}/workspaces", {"name": "Sarang", "parent": "agency-1"}),
        ("PATCH", f"{API}/workspaces/c1", {"spend_cap_cents_monthly": 2000}),
        ("GET", f"{API}/workspaces/c1/usage?month=2026-10", None),
        ("GET", f"{API}/workspaces/c1/members", None),
        ("POST", f"{API}/workspaces/c1/members", {"email": "guest@example.com"}),
        ("DELETE", f"{API}/workspaces/c1/members/u2", None),
        ("DELETE", f"{API}/workspaces/c1", None),
    ]


@responses.activate
def test_workspaces_create_in_account():
    responses.add(responses.POST, f"{API}/workspaces", json={"workspace": {"id": "w9"}}, status=201)
    Rymi().workspaces.create("Sarang", account="acct-1")
    assert json.loads(responses.calls[0].request.body) == {"name": "Sarang", "account": "acct-1"}


@responses.activate
def test_compliance_settings_and_billing_country():
    responses.add(responses.GET, f"{API}/compliance/settings", json={"configured": False})
    responses.add(responses.PUT, f"{API}/compliance/settings", json={"configured": True})
    responses.add(responses.GET, f"{API}/compliance/settings/preview", json={"changes": []})
    responses.add(responses.PUT, f"{API}/billing/country", json={"ok": True, "billing_country": "IN"})

    rymi = Rymi()
    rymi.compliance.get_settings()
    rymi.compliance.update_settings(operating_country="IN", rules={"apply_to_single_calls": True})
    rymi.compliance.preview_settings("US")
    rymi.billing.set_country("IN")

    sent = [(c.request.method, c.request.url, json.loads(c.request.body) if c.request.body else None) for c in responses.calls]
    assert sent == [
        ("GET", f"{API}/compliance/settings", None),
        ("PUT", f"{API}/compliance/settings", {"operating_country": "IN", "rules": {"apply_to_single_calls": True}}),
        ("GET", f"{API}/compliance/settings/preview?country=US", None),
        ("PUT", f"{API}/billing/country", {"billing_country": "IN"}),
    ]


@responses.activate
def test_update_settings_none_clears_the_country():
    responses.add(responses.PUT, f"{API}/compliance/settings", json={"configured": True})
    Rymi().compliance.update_settings(operating_country=None)
    Rymi().compliance.update_settings(rules={"dnc_check": True})
    assert json.loads(responses.calls[0].request.body) == {"operating_country": None}
    assert json.loads(responses.calls[1].request.body) == {"rules": {"dnc_check": True}}
