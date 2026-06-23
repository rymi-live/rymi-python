from typing import Any, Dict, Optional
from rymi.client import RymiClient

class NumbersResource:
    """Manage already-owned BYOC phone numbers registered with Rymi."""
    
    def __init__(self, client: RymiClient):
        self.client = client
        
    def list(self, **params: Any) -> Dict[str, Any]:
        """Retrieve a list of all assigned phone numbers."""
        return self.client.get("/numbers", params=params or None)

    def register(self, number: str, agent_id: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"number": number}
        if agent_id is not None:
            payload["agent_id"] = agent_id
        return self.client.post("/numbers", json=payload)

    def attach(self, number: str, agent_id: str) -> Dict[str, Any]:
        return self.client.post(f"/numbers/{number}/attach", json={"agent_id": agent_id})

    def remove(self, number: str) -> Dict[str, Any]:
        return self.client.delete(f"/numbers/{number}")
