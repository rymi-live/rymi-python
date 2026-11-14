import json
import os

import pytest
import responses

from rymi import Rymi


@pytest.fixture
def rymi_client():
    os.environ["RYMI_API_KEY"] = "rymi_test_123"
    return Rymi()


@responses.activate
def test_create_posts_only_given_fields(rymi_client):
    responses.add(responses.POST, "https://api.rymi.live/v1/bug-reports",
                  json={"bug_report": {"id": "b1", "status": "pending_review"}}, status=201)
    res = rymi_client.bug_reports.create("Voice cuts out", "The agent stops mid-sentence.", severity="high")
    assert res["bug_report"]["status"] == "pending_review"
    body = json.loads(responses.calls[0].request.body)
    assert body == {"title": "Voice cuts out", "description": "The agent stops mid-sentence.", "severity": "high"}


@responses.activate
def test_list_and_retrieve(rymi_client):
    responses.add(responses.GET, "https://api.rymi.live/v1/bug-reports",
                  json={"bug_reports": [], "total": 0, "limit": 5, "offset": 0}, status=200)
    responses.add(responses.GET, "https://api.rymi.live/v1/bug-reports/b1", json={"bug_report": {"id": "b1"}}, status=200)
    rymi_client.bug_reports.list(limit=5, status="fixed")
    assert "limit=5" in responses.calls[0].request.url and "status=fixed" in responses.calls[0].request.url
    assert rymi_client.bug_reports.retrieve("b1")["bug_report"]["id"] == "b1"
