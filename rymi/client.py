import os
import requests
from typing import Any, Dict, Optional
from urllib.parse import urlparse

class RymiError(Exception):
    """Custom exception raised for Rymi API Errors."""
    def __init__(self, message: str, status: Optional[int] = None, code: Optional[str] = None):
        super().__init__(message)
        self.status = status
        self.code = code

class RymiClient:
    """Core HTTP Client for the Rymi API."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.environ.get("RYMI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "The Rymi API Key must be set either by passing `api_key` to the client "
                "or setting the `RYMI_API_KEY` environment variable."
            )
            
        self.base_url = (base_url or "https://api.rymi.live/v1").rstrip("/")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "User-Agent": "rymi-python/1.0.0"
        })

    def request(self, method: str, path: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{path if path.startswith('/') else '/' + path}"
        
        try:
            response = self.session.request(method, url, json=json, params=params)
            
            # Attempt to parse JSON regardless of status code to check for error details
            data = None
            if "application/json" in response.headers.get("Content-Type", ""):
                try:
                    data = response.json()
                except ValueError:
                    data = response.text
            else:
                data = response.text

            if not response.ok:
                message = response.reason
                code = None
                
                if isinstance(data, dict):
                    message = data.get("error", message)
                    code = data.get("code")
                elif isinstance(data, str) and data:
                    message = data
                    
                raise RymiError(message, status=response.status_code, code=code)
                
            return data
            
        except requests.exceptions.RequestException as e:
            raise RymiError(f"Network Error: {str(e)}")

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("POST", path, json=json)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("PUT", path, json=json)
        
    def delete(self, path: str) -> Any:
        return self.request("DELETE", path)
