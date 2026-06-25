<div align="center">

# Rymi Python SDK

### The official Python wrapper for the [**Rymi**](https://rymi.live) Voice AI API — build and run AI voice agents from any Python app.

Manage agents (including multi-language and full model-stack control), phone numbers, calls, knowledge sources, evaluations, usage, and templates — plus webhook verification.

[![PyPI version](https://img.shields.io/pypi/v/rymi?color=6366f1&label=pypi&logo=pypi&logoColor=white)](https://pypi.org/project/rymi/)
[![Python versions](https://img.shields.io/pypi/pyversions/rymi?color=8b5cf6&logo=python&logoColor=white)](https://pypi.org/project/rymi/)
[![PyPI downloads](https://img.shields.io/pypi/dm/rymi?color=22d3ee&logo=pypi&logoColor=white)](https://pypi.org/project/rymi/)
[![license](https://img.shields.io/badge/license-MIT-22d3ee)](./LICENSE)

[**Documentation**](https://docs.rymi.live/api/sdk-python) · [**API Reference**](https://docs.rymi.live) · [**Dashboard**](https://rymi.live) · [**Node SDK**](https://www.npmjs.com/package/@rymi/node) · [**MCP Server**](https://www.npmjs.com/package/@rymi/mcp)

</div>

---

## ✨ Why Rymi

|   | |
|---|---|
| 🎙️ **Voice agents** | Full STT → LLM → TTS stack control, per-channel fallbacks, and multi-language support. |
| ☎️ **Telephony** | Register numbers, place outbound calls, and observe them live. |
| 📚 **Knowledge** | Ground agents in your own docs and data with managed knowledge sources. |
| 📊 **Usage & evals** | Track minutes and spend, then run evaluations to keep quality high. |
| 🔒 **Secure by default** | Built-in webhook signature verification; keys read from the environment. |

## 📦 Installation

```bash
pip install rymi
```

Requires **Python 3.8+**.

## 🚀 Quick Start

```python
import os
from rymi import Rymi

# Automatically picks up RYMI_API_KEY from the environment
client = Rymi()

# Or pass it explicitly
# client = Rymi(api_key="rymi_live_...")

agents = client.agents.list()
for agent in agents["agents"]:
    print(agent["name"])
```

> **Tip:** Keep your secret key in `RYMI_API_KEY` and let the client read it — never hard-code secret keys.

## 🧩 Resources

The client exposes one namespace per resource group:

| Namespace | What it does |
|-----------|--------------|
| `agents` | Create, update, clone, and configure voice agents |
| `calls` | Place, list, and observe calls; fetch transcripts and recordings |
| `numbers` | Register and attach phone numbers |
| `telephony` | Inspect carrier status and provisioned numbers |
| `keys` | Manage publishable keys |
| `billing` | Usage summaries and balance |
| `templates` | Prebuilt agent templates |
| `webhooks` | Create webhooks and verify incoming signatures |
| `dnc` | Do-not-call list management |

## 📖 Documentation

Full reference and guides: [**docs.rymi.live/api/sdk-python**](https://docs.rymi.live/api/sdk-python)

PyPI: [**pypi.org/project/rymi**](https://pypi.org/project/rymi/)

## 📄 License

[MIT](./LICENSE) © Rymi
