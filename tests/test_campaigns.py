import os
import pytest
import responses
from rymi import Rymi

API = "https://api.rymi.live/v1"


@pytest.fixture
def rymi_client():
    os.environ["RYMI_API_KEY"] = "rymi_test_123"
    return Rymi()


@responses.activate
def test_campaigns_and_contacts_resource_surface(rymi_client):
    """Parity surface: every CampaignsResource / ContactsResource method hits
    the right verb + path, mirroring the Node SDK 1:1."""
    cases = [
        # campaigns CRUD + lifecycle
        (responses.GET,    f"{API}/campaigns",                                  lambda c: c.campaigns.list()),
        (responses.POST,   f"{API}/campaigns",                                  lambda c: c.campaigns.create(agent_id="ag1", type="outbound", name="Q3 renewals")),
        (responses.GET,    f"{API}/campaigns/cmp1",                             lambda c: c.campaigns.retrieve("cmp1")),
        (responses.PATCH,  f"{API}/campaigns/cmp1",                             lambda c: c.campaigns.update("cmp1", name="Renamed")),
        (responses.POST,   f"{API}/campaigns/cmp1/launch",                      lambda c: c.campaigns.launch("cmp1")),
        (responses.GET,    f"{API}/campaigns/cmp1/launch-blockers",             lambda c: c.campaigns.launch_blockers("cmp1")),
        (responses.POST,   f"{API}/campaigns/cmp1/pause",                       lambda c: c.campaigns.pause("cmp1")),
        (responses.POST,   f"{API}/campaigns/cmp1/resume",                      lambda c: c.campaigns.resume("cmp1")),
        (responses.POST,   f"{API}/campaigns/cmp1/archive",                     lambda c: c.campaigns.archive("cmp1")),
        (responses.GET,    f"{API}/campaigns/cmp1/report",                      lambda c: c.campaigns.report("cmp1")),
        (responses.GET,    f"{API}/campaigns/cmp1/attempts",                    lambda c: c.campaigns.attempts("cmp1")),
        (responses.GET,    f"{API}/campaigns/cmp1/batches",                     lambda c: c.campaigns.batches("cmp1")),
        (responses.GET,    f"{API}/campaigns/cmp1/followups",                   lambda c: c.campaigns.followups("cmp1")),
        (responses.POST,   f"{API}/campaigns/cmp1/improve",                     lambda c: c.campaigns.improve("cmp1")),
        (responses.GET,    f"{API}/campaigns/cmp1/suggestions",                 lambda c: c.campaigns.suggestions("cmp1")),
        (responses.POST,   f"{API}/campaigns/cmp1/suggestions/sug1/accept",     lambda c: c.campaigns.accept_suggestion("cmp1", "sug1")),
        (responses.POST,   f"{API}/campaigns/cmp1/suggestions/sug1/dismiss",    lambda c: c.campaigns.dismiss_suggestion("cmp1", "sug1")),
        # campaign members (nested)
        (responses.GET,    f"{API}/campaigns/cmp1/members",                     lambda c: c.campaigns.members.list("cmp1")),
        (responses.POST,   f"{API}/campaigns/cmp1/members",                     lambda c: c.campaigns.members.add("cmp1", contact_ids=["ct1"])),
        (responses.POST,   f"{API}/campaigns/cmp1/members/import",              lambda c: c.campaigns.members.import_("cmp1", contacts=[{"phone": "+15551234567"}])),
        (responses.PATCH,  f"{API}/campaigns/cmp1/members/mem1",                lambda c: c.campaigns.members.update("cmp1", "mem1", status="opted_out")),
        (responses.DELETE, f"{API}/campaigns/cmp1/members/mem1",                lambda c: c.campaigns.members.remove("cmp1", "mem1")),
        # campaign inbound routes (nested)
        (responses.GET,    f"{API}/campaigns/cmp1/routes",                      lambda c: c.campaigns.routes.list("cmp1")),
        (responses.POST,   f"{API}/campaigns/cmp1/routes",                      lambda c: c.campaigns.routes.create("cmp1", phone_number="+15551234567")),
        (responses.PATCH,  f"{API}/campaigns/cmp1/routes/rt1",                  lambda c: c.campaigns.routes.update("cmp1", "rt1", active=False)),
        (responses.DELETE, f"{API}/campaigns/cmp1/routes/rt1",                  lambda c: c.campaigns.routes.remove("cmp1", "rt1")),
        # contacts
        (responses.GET,    f"{API}/contacts",                                   lambda c: c.contacts.list()),
        (responses.POST,   f"{API}/contacts",                                   lambda c: c.contacts.create(phone="+15551234567")),
        (responses.GET,    f"{API}/contacts/ct1",                               lambda c: c.contacts.retrieve("ct1")),
        (responses.PATCH,  f"{API}/contacts/ct1",                               lambda c: c.contacts.update("ct1", name="Jane")),
        (responses.DELETE, f"{API}/contacts/ct1",                               lambda c: c.contacts.delete("ct1")),
        (responses.POST,   f"{API}/contacts/import",                            lambda c: c.contacts.import_(contacts=[{"phone": "+15551234567"}])),
        (responses.PATCH,  f"{API}/contacts/ct1/consent",                       lambda c: c.contacts.set_consent("ct1", channel="voice", granted=True, source="web_form", method="checkbox")),
        # compliance
        (responses.POST,   f"{API}/compliance/attestations",                    lambda c: c.compliance.attest(kind="dnc_external_scrub", note="vendor X")),
        (responses.GET,    f"{API}/compliance/attestations",                    lambda c: c.compliance.list_attestations()),
    ]
    for verb, url, _ in cases:
        responses.add(verb, url, json={"ok": True}, status=200)

    for verb, url, call in cases:
        call(rymi_client)
        req = responses.calls[-1].request
        assert req.url.split("?")[0] == url, f"{url}: expected path {url}, got {req.url}"
        assert req.method == verb, f"{url}: expected {verb}, got {req.method}"
