# rymi (Python)

## 1.3.0

- Removed the four-tier role pricing from cost estimation. `billing.estimate()`
  now takes `stt_model` / `llm_model` / `tts_model` / `duration_seconds` instead
  of a `tier`, matching the two-track pricing model (managed SKUs vs custom
  agents at component cost + $0.02/min). The old `tier` argument was already
  ignored by the server.
- Removed the `agent_role` parameter from `agents.preview_stack()`. The
  stack-preview endpoint resolves stacks from languages and provider config; the
  `agent_role` argument was unused.
