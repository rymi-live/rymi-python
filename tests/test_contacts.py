import pytest
import responses

from rymi import Rymi

API = "https://api.rymi.live/v1"


@pytest.fixture(autouse=True)
def _env(monkeypatch):
    monkeypatch.setenv("RYMI_API_KEY", "rymi_test_123")
    monkeypatch.delenv("RYMI_WORKSPACE", raising=False)


@responses.activate
def test_contact_id_is_encoded_so_it_cannot_retarget_the_request():
    responses.add(responses.DELETE, f"{API}/contacts/..%2Fagents%2Fabc", json={})
    Rymi().contacts.delete("../agents/abc")
    assert responses.calls[0].request.url == f"{API}/contacts/..%2Fagents%2Fabc"
