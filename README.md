# Rymi Python SDK

The official Python wrapper for the Rymi Voice AI REST API. Manage agents (incl. multi-language and model-stack config), phone numbers, calls, knowledge sources, evaluations, usage, and templates, plus webhook verification.

Resources: `agents` · `calls` · `numbers` · `telephony` · `keys` · `billing` · `templates` · `webhooks`.

## Installation

```bash
pip install rymi
```

## Quick Start

```python
import os
from rymi import Rymi

# Automatically picks up RYMI_API_KEY from environment
client = Rymi()

# Or pass explicitly
# client = Rymi(api_key="rymi_live_...")

agents = client.agents.list()
for agent in agents["agents"]:
    print(agent['name'])
```
