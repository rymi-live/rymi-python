import json

import pytest
import responses

from rymi import Rymi

API = "https://api.rymi.live/v1"


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("RYMI_API_KEY", "rymi_test_123")
    monkeypatch.delenv("RYMI_WORKSPACE", raising=False)


@responses.activate
def test_accounts_resource_calls_the_right_routes():
    for method, url in [
        (responses.GET, f"{API}/accounts"),
        (responses.GET, f"{API}/accounts/acct%201"),
        (responses.PATCH, f"{API}/accounts/acct%201"),
        (responses.GET, f"{API}/accounts/acct%201/members"),
        (responses.POST, f"{API}/accounts/acct%201/members"),
        (responses.PATCH, f"{API}/accounts/acct%201/members/user%202"),
        (responses.DELETE, f"{API}/accounts/acct%201/members/user%202"),
        (responses.GET, f"{API}/accounts/acct%201/workspaces"),
    ]:
        responses.add(method, url, json={})

    rymi = Rymi()
    rymi.accounts.list()
    rymi.accounts.get("acct 1")
    rymi.accounts.update("acct 1", name="Sarang")
    rymi.accounts.list_members("acct 1")
    rymi.accounts.add_member("acct 1", "ada@example.com", "admin")
    rymi.accounts.update_member("acct 1", "user 2", "billing")
    rymi.accounts.remove_member("acct 1", "user 2")
    rymi.accounts.workspaces("acct 1")

    sent = [
        (c.request.method, c.request.url, json.loads(c.request.body) if c.request.body else None)
        for c in responses.calls
    ]
    assert sent == [
        ("GET", f"{API}/accounts", None),
        ("GET", f"{API}/accounts/acct%201", None),
        ("PATCH", f"{API}/accounts/acct%201", {"name": "Sarang"}),
        ("GET", f"{API}/accounts/acct%201/members", None),
        ("POST", f"{API}/accounts/acct%201/members", {"email": "ada@example.com", "role": "admin"}),
        ("PATCH", f"{API}/accounts/acct%201/members/user%202", {"role": "billing"}),
        ("DELETE", f"{API}/accounts/acct%201/members/user%202", None),
        ("GET", f"{API}/accounts/acct%201/workspaces", None),
    ]


@responses.activate
def test_keys_create_and_self():
    responses.add(responses.POST, f"{API}/auth/api-keys", json={"key": "rymi_ws_secret"}, status=201)
    responses.add(responses.GET, f"{API}/keys/self", json={"kind": "workspace", "scopes": ["calls:read"], "legacy": False})

    rymi = Rymi()
    created = rymi.keys.create(kind="workspace", scopes=["calls:read", "calls:write"], label="Dialler")
    self_key = rymi.keys.self()
    assert created["key"] == "rymi_ws_secret"
    assert self_key["scopes"] == ["calls:read"]

    sent = [
        (c.request.method, c.request.url, json.loads(c.request.body) if c.request.body else None)
        for c in responses.calls
    ]
    assert sent == [
        ("POST", f"{API}/auth/api-keys", {"kind": "workspace", "scopes": ["calls:read", "calls:write"], "label": "Dialler"}),
        ("GET", f"{API}/keys/self", None),
    ]
