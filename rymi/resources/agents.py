from typing import Any, Dict, List, Optional
from rymi.client import RymiClient

class AgentsResource:
    """Manage AI Agents."""
    
    def __init__(self, client: RymiClient):
        self.client = client
        
    def list(self, **params: Any) -> Dict[str, Any]:
        """Retrieve a list of all your AI Agents."""
        return self.client.get("/agents", params=params or None)
        
    def retrieve(self, agent_id: str) -> Dict[str, Any]:
        """Retrieve a single AI Agent by its unique ID."""
        return self.client.get(f"/agents/{agent_id}")
        
    def create(self, name: str, system_prompt: Optional[str] = None, voice: Optional[str] = None, language: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        """Create a new AI Agent."""
        prompt = kwargs.pop("prompt", None)
        payload = {"name": name}
        if system_prompt or prompt:
            payload["system_prompt"] = system_prompt or prompt
        if voice:
            payload["voice"] = voice
        if language:
            payload["language"] = language
        payload.update(kwargs)
            
        return self.client.post("/agents", json=payload)
        
    def update(self, agent_id: str, name: Optional[str] = None, system_prompt: Optional[str] = None, voice: Optional[str] = None, language: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        """Update an existing AI Agent."""
        prompt = kwargs.pop("prompt", None)
        payload = {}
        if name: payload["name"] = name
        if system_prompt or prompt: payload["system_prompt"] = system_prompt or prompt
        if voice: payload["voice"] = voice
        if language: payload["language"] = language
        payload.update(kwargs)
            
        return self.client.put(f"/agents/{agent_id}", json=payload)
        
    def delete(self, agent_id: str) -> Dict[str, Any]:
        """Delete an AI Agent permanently."""
        return self.client.delete(f"/agents/{agent_id}")

    def llm_options(self) -> Dict[str, Any]:
        """Retrieve model and voice catalog options."""
        return self.client.get("/agents/llm-options")

    def generate(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a structured agent draft from a plain-English brief."""
        payload: Dict[str, Any] = {"prompt": prompt}
        if options:
            payload["options"] = options
        return self.client.post("/agents/generate", json=payload)

    def list_calls(self, agent_id: str, limit: int = 50, offset: int = 0, status: Optional[str] = None) -> Dict[str, Any]:
        """List calls made with a specific agent."""
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        return self.client.get(f"/agents/{agent_id}/calls", params=params)

    def clone(self, agent_id: str) -> Dict[str, Any]:
        """Duplicate an existing agent. The copy gets ' (Copy)' appended to its name."""
        return self.client.post(f"/agents/{agent_id}/clone", json={})

    def validate_publish(self, agent_id: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        """Check whether an agent is ready to go live without persisting changes."""
        payload: Dict[str, Any] = {}
        if agent_id:
            payload["agent_id"] = agent_id
        payload.update(kwargs)
        return self.client.post("/agents/validate-publish", json=payload)

    def apply_changes(self, current_config: Dict[str, Any], changes: list, mode: str = "edit", lenient: bool = False) -> Dict[str, Any]:
        """Validate and resolve a flat key/value change-set. Does NOT persist — follow up with update()."""
        return self.client.post("/agents/apply-changes", json={
            "currentConfig": current_config,
            "changes": changes,
            "mode": mode,
            "lenient": lenient,
        })

    def enrich_company(self, company_name: str, website_url: str) -> Dict[str, Any]:
        """Auto-generate a company description from a website URL using AI + Google Search."""
        return self.client.post("/agents/enrich-company", json={
            "companyName": company_name,
            "websiteUrl": website_url,
        })

    def preview_stack(
        self,
        supported_languages: List[str],
        language: Optional[str] = None,
        current_provider_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolve the model stack (STT/LLM/TTS), blockers, and warnings for a set of
        supported languages without saving."""
        payload: Dict[str, Any] = {"supported_languages": supported_languages}
        if language is not None:
            payload["language"] = language
        if current_provider_config is not None:
            payload["current_provider_config"] = current_provider_config
        return self.client.post("/agents/stack-preview", json=payload)

    def list_knowledge_sources(self, agent_id: str) -> Dict[str, Any]:
        """List the knowledge sources (RAG context) attached to an agent."""
        return self.client.get(f"/agents/{agent_id}/knowledge-sources")

    def add_knowledge_source(
        self,
        agent_id: str,
        kind: str,
        title: str,
        text: Optional[str] = None,
        url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add a knowledge source from raw text (kind='text') or a URL (kind='url')."""
        payload: Dict[str, Any] = {"kind": kind, "title": title}
        if text is not None:
            payload["text"] = text
        if url is not None:
            payload["url"] = url
        return self.client.post(f"/agents/{agent_id}/knowledge-sources", json=payload)

    def delete_knowledge_source(self, agent_id: str, source_id: str) -> Dict[str, Any]:
        """Delete a knowledge source from an agent."""
        return self.client.delete(f"/agents/{agent_id}/knowledge-sources/{source_id}")

    def list_changes(self, agent_id: str, since: Optional[str] = None) -> Dict[str, Any]:
        """List recorded configuration changes for an agent (optionally since an ISO timestamp)."""
        params = {"since": since} if since else None
        return self.client.get(f"/agents/{agent_id}/changes", params=params)

    def undo_change(self, agent_id: str, change_id: str) -> Dict[str, Any]:
        """Undo a single recorded configuration change, reverting that field to its previous value."""
        return self.client.post(f"/agents/{agent_id}/changes/{change_id}/undo", json={})

    def run_evals(self, agent_id: str, mode: Optional[str] = None) -> Dict[str, Any]:
        """Run the evaluation suite for an agent. mode='synthetic' (default) or 'live'."""
        path = f"/agents/{agent_id}/evals/run"
        if mode:
            path += f"?mode={mode}"
        return self.client.post(path, json={})

    def list_eval_runs(self, agent_id: str) -> Dict[str, Any]:
        """List previous evaluation runs for an agent."""
        return self.client.get(f"/agents/{agent_id}/evals/runs")

    def get_eval_run(self, agent_id: str, run_id: str) -> Dict[str, Any]:
        """Retrieve a single evaluation run, including per-scenario scores."""
        return self.client.get(f"/agents/{agent_id}/evals/runs/{run_id}")
