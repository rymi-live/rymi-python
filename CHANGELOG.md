# rymi (Python)

## Unreleased

- **Breaking:** a workspace's `role` and a workspace member's `role` are no longer `owner`. Workspace roles are `admin`, `editor`, `client` and `viewer`; a workspace's `role` is `None` for a Billing member with no workspace role.
- **Breaking:** `billing.set_auto_recharge`, `set_alerts` and `set_country` return `403` for every API key. Top up and change billing in Studio.
- Accounts and scoped keys: `accounts.list`, `get`, `update`, `list_members`, `add_member`, `update_member`, `remove_member`, and `workspaces`; `keys.create(kind=, scopes=, label=)` and `keys.self()`.
- `workspaces.create(name, account=...)` creates the workspace in that account. `accounts.update_member` returns `{"member": {"user_id", "role"}}`, with no `email`.

## 1.6.0

- `workspaces.delete(workspace_id)` deletes an empty workspace. Owner only, never your first workspace (`400` `cannot_delete_primary`); `409` `workspace_not_empty` lists the `blockers`.

## 1.5.0

- `Rymi(workspace=…)`, the `RYMI_WORKSPACE` environment variable, and `with_workspace(id)` send `Rymi-Workspace` on every request.
- New `workspaces` resource: `list`, `create` (including `parent` for a client workspace), `update`, `usage`, `list_members`, `add_member`, `remove_member`.
- Compliance settings: `compliance.get_settings`, `update_settings`, and `preview_settings`. `update_settings(operating_country=None)` clears the country.
- `billing.set_country` sets the billing country. Locked after the first paid invoice (`409` `billing_country_locked`).

## 1.4.0

- `campaigns.intake.get / set / rotate / disable` for a campaign's lead-intake URL.
- `agents.get_share_link / set_share_link / regenerate_share_link` for an agent's public share link.
- New `tool_secrets` resource (`list`, `set(name, value, host)`, `delete`) for API-tool header secrets referenced as `{{secrets.NAME}}`, matching the Node SDK.

## 1.3.0

- Removed the four-tier role pricing from cost estimation. `billing.estimate()`
  now takes `stt_model` / `llm_model` / `tts_model` / `duration_seconds` instead
  of a `tier`, matching the two-track pricing model (managed SKUs vs custom
  agents at component cost + $0.02/min). The old `tier` argument was already
  ignored by the server.
- Removed the `agent_role` parameter from `agents.preview_stack()`. The
  stack-preview endpoint resolves stacks from languages and provider config; the
  `agent_role` argument was unused.
