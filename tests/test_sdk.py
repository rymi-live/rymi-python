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
