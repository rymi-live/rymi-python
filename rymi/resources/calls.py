from typing import Any, Dict, List, Optional
from rymi.client import RymiClient

class CallsResource:
    """Manage Outbound Calls."""
    
    def __init__(self, client: RymiClient):
        self.client = client
        
    def list(self, **params: Any) -> Dict[str, Any]:
        """Retrieve a list of all call records."""
        return self.client.get("/calls", params=params or None)

    def active(self, **params: Any) -> Dict[str, Any]:
        """Retrieve active in-progress calls."""
        return self.client.get("/calls/active", params=params or None)
        
    def retrieve(self, call_id: str) -> Dict[str, Any]:
        """Retrieve a single call record and transcript."""
        return self.client.get(f"/calls/{call_id}")
        
    def create(
        self,
        agent_id: str,
        participants: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
        post_call: Optional[Dict[str, Any]] = None,
        to: Optional[str] = None,
        from_number: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a WebRTC/PSTN call using the participant-first API."""
        if participants is None and to:
            participants = [{
                "transport": "pstn",
                "identity": to,
                "from_number": from_number
            }]

        payload = {
            "agent_id": agent_id,
            "participants": participants or []
        }
        if metadata:
            payload["metadata"] = metadata
        if variables:
            payload["variables"] = variables
        if post_call:
            payload["post_call"] = post_call
            
        return self.client.post("/calls", json=payload)

    def batch(self, agent_id: str, to: List[str], from_number: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        """Queue a batch of outbound PSTN recipients."""
        payload = {"agent_id": agent_id, "to": to}
        if from_number:
            payload["from_number"] = from_number
        payload.update(kwargs)
        return self.client.post("/calls/batch", json=payload)

    def summary(self, call_id: str) -> Dict[str, Any]:
        return self.client.get(f"/calls/{call_id}/summary")

    def transcript(self, call_id: str) -> Dict[str, Any]:
        return self.client.get(f"/calls/{call_id}/transcript")

    def recording(self, call_id: str) -> Dict[str, Any]:
        return self.client.get(f"/calls/{call_id}/recording")

    def reprocess(self, call_id: str) -> Dict[str, Any]:
        return self.client.post(f"/calls/{call_id}/reprocess")

    def end(self, call_id: str) -> Dict[str, Any]:
        """End an in-progress call."""
        return self.client.post(f"/calls/{call_id}/end")

    def add_participants(self, call_id: str, participants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add one or more participants to a live call (warm transfer / conference)."""
        return self.client.post(f"/calls/{call_id}/participants", json={"participants": participants})

    def queue_stats(self) -> Dict[str, Any]:
        return self.client.get("/calls/queue/stats")
