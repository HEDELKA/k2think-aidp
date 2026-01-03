"""K2Think AI Client - Python version for AIDP GPU Compute

OpenAI-compatible client for K2Think platform with GPU monitoring.
"""

import requests
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Message:
    """Chat message"""
    role: str  # "user" or "assistant"
    content: str


class K2ThinkClient:
    """K2Think API Client"""
    
    def __init__(self, 
                 email: Optional[str] = None, 
                 password: Optional[str] = None,
                 api_base: str = "https://www.k2think.ai"):
        self.email = email or os.getenv("K2THINK_EMAIL")
        self.password = password or os.getenv("K2THINK_PASSWORD")
        self.api_base = api_base
        self.token = None
        self.session = requests.Session()
        
        if not self.email or not self.password:
            raise ValueError("K2Think credentials required (email/password or env vars)")
    
    def authenticate(self) -> bool:
        """Authenticate and get access token"""
        try:
            response = self.session.post(
                f"{self.api_base}/api/auth/login",
                json={
                    "email": self.email,
                    "password": self.password
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                })
                return True
            else:
                print(f"Auth failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def chat_completion(self,
                       model: str = "MBZUAI-IFM/K2-Think",
                       messages: Optional[List[Dict]] = None,
                       max_tokens: int = 500,
                       temperature: float = 0.7) -> Dict[str, Any]:
        """Create chat completion (OpenAI-compatible)"""
        
        if not self.token:
            if not self.authenticate():
                raise RuntimeError("Failed to authenticate")
        
        if messages is None:
            messages = []
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = self.session.post(
                f"{self.api_base}/api/chat/completions",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"API error {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {"error": f"Request failed: {e}"}
    
    def list_models(self) -> List[Dict]:
        """List available models"""
        if not self.token:
            if not self.authenticate():
                return []
        
        try:
            response = self.session.get(
                f"{self.api_base}/api/v1/models",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", []) if isinstance(data, dict) else data
            return []
        except Exception as e:
            print(f"Failed to list models: {e}")
            return []
    
    def simple_ask(self, question: str, max_tokens: int = 200) -> str:
        """Simple helper for single question"""
        response = self.chat_completion(
            messages=[{"role": "user", "content": question}],
            max_tokens=max_tokens
        )
        
        if "error" in response:
            return f"Error: {response['error']}"
        
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return f"Unexpected response format: {response}"
