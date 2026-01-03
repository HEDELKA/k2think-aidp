"""
K2Think AI Client - Fixed Version with Better Error Handling

OpenAI-compatible client for K2Think platform with GPU monitoring.
"""

import requests
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import os
from dotenv import load_dotenv
import time

load_dotenv()


class K2ThinkClient:
    """K2Think API Client with improved error handling"""
    
    def __init__(self, 
                 email: Optional[str] = None, 
                 password: Optional[str] = None,
                 api_base: str = "https://www.k2think.ai",
                 debug: bool = True):
        self.email = email or os.getenv("K2THINK_EMAIL")
        self.password = password or os.getenv("K2THINK_PASSWORD")
        self.api_base = api_base
        self.token = None
        self.session = requests.Session()
        self.debug = debug
        
        if not self.email or not self.password:
            raise ValueError("❌ K2Think credentials required (email/password or env vars)")
        
        if self.debug:
            print(f"[K2Think] Initializing client for: {self.email}")
            print(f"[K2Think] API Base: {self.api_base}")
    
    def authenticate(self) -> bool:
        """Authenticate and get access token"""
        try:
            if self.debug:
                print("[K2Think] Attempting authentication...")
            
            auth_url = f"{self.api_base}/api/auth/login"
            
            if self.debug:
                print(f"[K2Think] POST {auth_url}")
            
            response = self.session.post(
                auth_url,
                json={
                    "email": self.email,
                    "password": self.password
                },
                timeout=15
            )
            
            if self.debug:
                print(f"[K2Think] Response status: {response.status_code}")
                print(f"[K2Think] Response headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token") or data.get("token")
                
                if not self.token:
                    print(f"[K2Think] ⚠️  No token in response: {data}")
                    return False
                
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                })
                
                if self.debug:
                    print(f"[K2Think] ✓ Authenticated successfully")
                    print(f"[K2Think] Token: {self.token[:20]}...")
                
                return True
            
            elif response.status_code == 401:
                print(f"[K2Think] ❌ 401 Unauthorized - Check credentials")
                print(f"[K2Think] Response: {response.text}")
                return False
            
            elif response.status_code == 400:
                print(f"[K2Think] ❌ 400 Bad Request")
                try:
                    error_data = response.json()
                    print(f"[K2Think] Error: {error_data}")
                except:
                    print(f"[K2Think] Response: {response.text}")
                return False
            
            else:
                print(f"[K2Think] ❌ Authentication failed: {response.status_code}")
                print(f"[K2Think] Response: {response.text[:200]}")
                return False
        
        except requests.exceptions.Timeout:
            print(f"[K2Think] ❌ Request timeout - K2Think service may be down")
            return False
        
        except requests.exceptions.ConnectionError as e:
            print(f"[K2Think] ❌ Connection error: {e}")
            return False
        
        except Exception as e:
            print(f"[K2Think] ❌ Authentication error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def chat_completion(self,
                       model: str = "MBZUAI-IFM/K2-Think",
                       messages: Optional[List[Dict]] = None,
                       max_tokens: int = 500,
                       temperature: float = 0.7) -> Dict[str, Any]:
        """Create chat completion (OpenAI-compatible)"""
        
        if messages is None:
            messages = []
        
        # First authentication attempt
        if not self.token:
            if self.debug:
                print("[K2Think] No token, authenticating...")
            
            if not self.authenticate():
                raise RuntimeError("❌ Failed to authenticate with K2Think")
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            completion_url = f"{self.api_base}/api/chat/completions"
            
            if self.debug:
                print(f"[K2Think] POST {completion_url}")
                print(f"[K2Think] Messages: {len(messages)}")
                print(f"[K2Think] Max tokens: {max_tokens}")
            
            response = self.session.post(
                completion_url,
                json=payload,
                timeout=60
            )
            
            if self.debug:
                print(f"[K2Think] Response status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 401:
                # Token expired, try to reauthenticate
                print(f"[K2Think] Token expired, re-authenticating...")
                self.token = None
                
                if self.authenticate():
                    return self.chat_completion(
                        model=model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature
                    )
                else:
                    return {"error": "Re-authentication failed"}
            
            elif response.status_code == 429:
                print(f"[K2Think] ⚠️  Rate limited - waiting 5 seconds...")
                time.sleep(5)
                return self.chat_completion(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
            
            else:
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", response.text)
                except:
                    error_msg = response.text
                
                return {
                    "error": f"API error {response.status_code}: {error_msg}"
                }
        
        except requests.exceptions.Timeout:
            return {"error": "Request timeout - API may be overloaded"}
        
        except requests.exceptions.ConnectionError as e:
            return {"error": f"Connection error: {e}"}
        
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
            print(f"[K2Think] Failed to list models: {e}")
            return []
    
    def simple_ask(self, question: str, max_tokens: int = 200) -> str:
        """Simple helper for single question"""
        response = self.chat_completion(
            messages=[{"role": "user", "content": question}],
            max_tokens=max_tokens
        )
        
        if "error" in response:
            return f"❌ Error: {response['error']}"
        
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return f"Unexpected response format: {response}"


# Demo function
def test_client():
    """Test K2Think client"""
    print("\n🧪 Testing K2Think Client\n")
    
    try:
        client = K2ThinkClient(debug=True)
        
        print("\n📝 Sending test request...\n")
        response = client.chat_completion(
            messages=[{
                "role": "user",
                "content": "Say 'Hello from K2Think!' in one sentence"
            }],
            max_tokens=50
        )
        
        if "error" not in response:
            text = response["choices"][0]["message"]["content"]
            print(f"\n✅ Response: {text}\n")
            return True
        else:
            print(f"\n❌ Error: {response['error']}\n")
            return False
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}\n")
        return False


if __name__ == "__main__":
    test_client()
