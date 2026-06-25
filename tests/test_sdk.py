import os
import time
import pytest
import responses
import hmac
import hashlib
import json
from rymi import Rymi, RymiError

@pytest.fixture
def rymi_client():
    os.environ["RYMI_API_KEY"] = "rymi_test_123"
    return Rymi()

@responses.activate
def test_client_authentication(rymi_client):
    responses.add(
        responses.GET,
        "https://api.rymi.live/v1/agents",
        json={"agents": [{"id": "agent_1"}], "total": 1, "offset": 0, "limit": 50},
        status=200
    )
    
    agents = rymi_client.agents.list()
    assert len(agents["agents"]) == 1
    assert agents["agents"][0]["id"] == "agent_1"
    
    # Verify headers
    req = responses.calls[0].request
    assert req.headers["Authorization"] == "Bearer rymi_test_123"
    assert req.headers["Accept"] == "application/json"

@responses.activate
def test_client_error_handling(rymi_client):
    responses.add(
        responses.POST,
        "https://api.rymi.live/v1/calls",
        json={"error": "Agent not found", "code": "not_found"},
        status=404
    )
    
    with pytest.raises(RymiError) as exc_info:
        rymi_client.calls.create(agent_id="bad_id", to="+123", from_number="+123")
        
    assert "Agent not found" in str(exc_info.value)
    assert exc_info.value.status == 404
    assert exc_info.value.code == "not_found"

def test_webhook_signature_verification(rymi_client):
    secret = "whsec_test_secret"
    payload = json.dumps({"type": "call.ended", "call_id": "call_123"})
    timestamp = str(int(time.time() * 1000))
    
    # Generate valid signature
    signature_payload = f"{timestamp}.{payload}"
    signature = hmac.new(
        secret.encode('utf-8'),
        signature_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Should pass
    assert rymi_client.webhooks.verify_signature(payload, signature, timestamp, secret) is True
    
    # Should fail bad signature
    with pytest.raises(ValueError, match="Invalid Webhook Signature"):
        rymi_client.webhooks.verify_signature(payload, "bad_signature", timestamp, secret)
        
    # Should fail replay attack
    old_timestamp = str(int(time.time() * 1000) - 600000) # 10 mins ago
    old_signature = hmac.new(
        secret.encode('utf-8'),
        f"{old_timestamp}.{payload}".encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    with pytest.raises(ValueError, match="Possible replay attack"):
        rymi_client.webhooks.verify_signature(payload, old_signature, old_timestamp, secret)


API = "https://api.rymi.live/v1"


@responses.activate
def test_extended_resource_surface(rymi_client):
    """Parity surface: DNC, call control, key create/revoke, billing controls,
    telephony connect/disconnect, and webhook CRUD hit the right verb + path."""
    cases = [
        (responses.POST,   f"{API}/dnc",                    lambda c: c.dnc.add(phone_number="+15551234567")),
        (responses.POST,   f"{API}/dnc/batch",              lambda c: c.dnc.add_batch(phone_numbers=["+15551234567"])),
        (responses.POST,   f"{API}/dnc/check",              lambda c: c.dnc.check(phone_numbers=["+15551234567"])),
        (responses.GET,    f"{API}/dnc",                    lambda c: c.dnc.list()),
        (responses.DELETE, f"{API}/dnc/+15551234567",       lambda c: c.dnc.remove("+15551234567")),
        (responses.POST,   f"{API}/calls/abc/end",          lambda c: c.calls.end("abc")),
        (responses.POST,   f"{API}/calls/abc/participants", lambda c: c.calls.add_participants("abc", [{"transport": "pstn", "identity": "+1"}])),
        (responses.POST,   f"{API}/keys/publishable",       lambda c: c.keys.create_publishable(agent_id="ag1", label="x")),
        (responses.DELETE, f"{API}/keys/publishable/k1",    lambda c: c.keys.revoke_publishable("k1")),
        (responses.POST,   f"{API}/billing/estimate",       lambda c: c.billing.estimate(llm_model="gemini-2.5-flash", duration_seconds=300)),
        (responses.PUT,    f"{API}/billing/auto-recharge",  lambda c: c.billing.set_auto_recharge(enabled=True)),
        (responses.PUT,    f"{API}/billing/alerts",         lambda c: c.billing.set_alerts(low_balance_pct=15)),
        (responses.POST,   f"{API}/telephony/connect",      lambda c: c.telephony.connect(provider="twilio", auth_id="AC")),
        (responses.POST,   f"{API}/telephony/disconnect",   lambda c: c.telephony.disconnect()),
        (responses.GET,    f"{API}/webhooks",               lambda c: c.webhooks.list()),
        (responses.POST,   f"{API}/webhooks",               lambda c: c.webhooks.create(url="https://x", events=["call.completed"], secret="whsec_x")),
        (responses.PATCH,  f"{API}/webhooks/wh1",           lambda c: c.webhooks.update("wh1", events=["call.completed"])),
        (responses.DELETE, f"{API}/webhooks/wh1",           lambda c: c.webhooks.delete("wh1")),
    ]
    for verb, url, _ in cases:
        responses.add(verb, url, json={"ok": True}, status=200)

    for verb, url, call in cases:
        call(rymi_client)
        req = responses.calls[-1].request
        assert req.method == verb, f"{url}: expected {verb}, got {req.method}"
