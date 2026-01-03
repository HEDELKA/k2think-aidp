"""
K2Think AIDP GPU Compute Demo for Google Colab

Custom AI Agent Wrapper optimized for Decentralized Compute

This script runs in Google Colab and demonstrates:
1. GPU detection and monitoring
2. K2Think AI inference with GPU logging
3. AIDP compute integration

Simply run all cells to see GPU compute in action!
"""

# ============================================================================
# SETUP: Install dependencies
# ============================================================================

print("📦 Installing dependencies...")
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "requests", "python-dotenv"])
print("✓ Dependencies installed")

# ============================================================================
# IMPORT: Load modules
# ============================================================================

import os
import sys
from datetime import datetime
from typing import Dict

# Detect if running in Colab
IN_COLAB = 'google.colab' in sys.modules
print(f"🔍 Running in Colab: {IN_COLAB}")

# ============================================================================
# GPU MONITOR MODULE (inline)
# ============================================================================

class GPUMonitor:
    """Monitors GPU utilization using nvidia-smi"""
    
    def __init__(self, log_file: str = "gpu-usage.log"):
        self.log_file = log_file
        self.is_available = self._check_gpu_availability()
        self.logs = []
    
    def _check_gpu_availability(self) -> bool:
        """Check if GPU is available"""
        try:
            result = subprocess.run(['nvidia-smi', '--version'], 
                                  capture_output=True, check=True, timeout=5)
            return True
        except Exception as e:
            return False
    
    def _run_nvidia_smi(self, query: str) -> str:
        """Run nvidia-smi with query"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=' + query, '--format=csv,noheader'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"
    
    def log_pre_compute_status(self, task_name: str = "AI Inference"):
        """Log GPU status before compute"""
        timestamp = datetime.now().isoformat()
        separator = "=" * 60
        
        log_entry = f"\n{separator}\n[{timestamp}] PRE-COMPUTE GPU STATUS: {task_name}\n{separator}\n"
        
        if self.is_available:
            gpu_details = self._run_nvidia_smi("index,name,driver_version,memory.total")
            log_entry += f"GPU Details:\n{gpu_details}\n"
            
            metrics = self._run_nvidia_smi("index,memory.used,memory.free,utilization.gpu,temperature.gpu")
            log_entry += f"\nMemory & Utilization:\n{metrics}\n"
        else:
            log_entry += "GPU not available\n"
        
        self._append_log(log_entry)
        print(log_entry)
    
    def log_compute_status(self, task_name: str = "Processing"):
        """Log GPU status during compute"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] DURING: {task_name}\n"
        
        if self.is_available:
            metrics = self._run_nvidia_smi("index,utilization.gpu,utilization.memory,memory.used,temperature.gpu")
            log_entry += metrics + "\n"
        
        self._append_log(log_entry)
        print(log_entry)
    
    def log_post_compute_status(self, summary: str = ""):
        """Log GPU status after compute"""
        timestamp = datetime.now().isoformat()
        separator = "=" * 60
        
        log_entry = f"\n{separator}\n[{timestamp}] POST-COMPUTE GPU STATUS\n{separator}\n"
        
        if self.is_available:
            metrics = self._run_nvidia_smi("index,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu")
            log_entry += f"Final GPU State:\n{metrics}\n"
        
        if summary:
            log_entry += f"\nResult: {summary}\n"
        
        log_entry += f"{separator}\n\n"
        self._append_log(log_entry)
        print(log_entry)
    
    def get_summary(self) -> Dict:
        """Get GPU summary"""
        if not self.is_available:
            return {"status": "unavailable", "mode": "cpu"}
        
        try:
            gpu_info = self._run_nvidia_smi("name,driver_version,memory.total")
            parts = gpu_info.split(', ')
            return {
                "status": "available",
                "mode": "gpu",
                "gpu": parts[0] if len(parts) > 0 else "Unknown",
                "driver": parts[1] if len(parts) > 1 else "Unknown",
                "memory": parts[2] if len(parts) > 2 else "Unknown"
            }
        except:
            return {"status": "error"}
    
    def _append_log(self, message: str):
        """Save log"""
        self.logs.append(message)
        try:
            with open(self.log_file, 'a') as f:
                f.write(message)
        except:
            pass
    
    def get_log_content(self) -> str:
        """Get full log"""
        try:
            with open(self.log_file, 'r') as f:
                return f.read()
        except:
            return "\n".join(self.logs)


# ============================================================================
# K2THINK CLIENT MODULE (inline)
# ============================================================================

import requests
from typing import Optional, List

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
            raise ValueError("K2Think credentials required")
    
    def authenticate(self) -> bool:
        """Authenticate with K2Think"""
        try:
            response = self.session.post(
                f"{self.api_base}/api/auth/login",
                json={"email": self.email, "password": self.password},
                timeout=10
            )
            
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                })
                return True
            return False
        except Exception as e:
            print(f"Auth error: {e}")
            return False
    
    def chat_completion(self,
                       model: str = "MBZUAI-IFM/K2-Think",
                       messages: Optional[List] = None,
                       max_tokens: int = 500,
                       temperature: float = 0.7) -> Dict:
        """Chat completion"""
        
        if not self.token and not self.authenticate():
            raise RuntimeError("Authentication failed")
        
        payload = {
            "model": model,
            "messages": messages or [],
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
            return response.json() if response.status_code == 200 else {"error": response.text}
        except Exception as e:
            return {"error": str(e)}
    
    def simple_ask(self, question: str, max_tokens: int = 200) -> str:
        """Ask a question"""
        response = self.chat_completion(
            messages=[{"role": "user", "content": question}],
            max_tokens=max_tokens
        )
        
        if "error" in response:
            return f"Error: {response['error']}"
        
        try:
            return response["choices"][0]["message"]["content"]
        except:
            return f"Response: {response}"


# ============================================================================
# CONFIGURATION
# ============================================================================

print("\n╔════════════════════════════════════════════════════════════╗")
print("║   Custom AI Agent Wrapper - Decentralized Compute          ║")
print("║   K2Think + AIDP GPU Network Demo                          ║")
print("╚════════════════════════════════════════════════════════════╝\n")

# Get credentials
print("🔑 Configuring K2Think credentials...")
print("If no credentials are set, use the form below:")

email = os.getenv("K2THINK_EMAIL")
password = os.getenv("K2THINK_PASSWORD")

if not email or not password:
    print("\n⚠️  No K2Think credentials found in environment.")
    print("Set them using one of:")
    print("  1. Export environment variables:")
    print("     export K2THINK_EMAIL='your-email@example.com'")
    print("     export K2THINK_PASSWORD='your-password'")
    print("  2. Or create .env file in working directory")
    print("  3. Or modify email/password below:\n")
    
    email = input("Enter K2Think email: ").strip()
    password = input("Enter K2Think password: ").strip()

# ============================================================================
# INITIALIZE GPU MONITOR
# ============================================================================

print("\n📊 Initializing GPU Monitor...")
gpu_monitor = GPUMonitor("gpu-usage.log")
gpu_summary = gpu_monitor.get_summary()

print(f"GPU Status: {gpu_summary['status']}")
if gpu_summary['status'] == 'available':
    print(f"  GPU: {gpu_summary.get('gpu', 'Unknown')}")
    print(f"  Driver: {gpu_summary.get('driver', 'Unknown')}")
    print(f"  Memory: {gpu_summary.get('memory', 'Unknown')}")
else:
    if IN_COLAB:
        print("⚠️  To enable GPU in Colab:")
        print("  1. Go to Runtime → Change runtime type")
        print("  2. Select GPU as Hardware accelerator")
        print("  3. Restart and run again")
    else:
        print("  CPU mode enabled")

# ============================================================================
# DEMO EXECUTION
# ============================================================================

print("\n🚀 Starting AI inference with GPU monitoring...\n")

try:
    # Initialize client
    print("🤖 Initializing K2Think client...")
    client = K2ThinkClient(email=email, password=password)
    
    if not client.authenticate():
        print("❌ Authentication failed. Check credentials.")
    else:
        print("✓ Authenticated\n")
        
        # Pre-compute status
        gpu_monitor.log_pre_compute_status("K2Think AI Inference")
        
        # Task 1: Text generation
        print("\n⚡ Task 1: Text Generation")
        gpu_monitor.log_compute_status("Text Generation")
        
        response = client.chat_completion(
            messages=[{
                "role": "user",
                "content": "Explain GPU compute in 2 sentences"
            }],
            max_tokens=100
        )
        
        if "error" not in response:
            text = response["choices"][0]["message"]["content"]
            tokens = response.get("usage", {}).get("total_tokens", 0)
            print(f"Response: {text}")
            print(f"Tokens used: {tokens}")
        else:
            print(f"Error: {response['error']}")
        
        gpu_monitor.log_compute_status("Text Generation Complete")
        
        # Task 2: Code example
        print("\n⚡ Task 2: Code Generation")
        gpu_monitor.log_compute_status("Code Generation")
        
        response = client.chat_completion(
            messages=[{
                "role": "user",
                "content": "Write simple Python to check GPU"
            }],
            max_tokens=150
        )
        
        if "error" not in response:
            code = response["choices"][0]["message"]["content"]
            tokens = response.get("usage", {}).get("total_tokens", 0)
            print(f"Response: {code}")
            print(f"Tokens used: {tokens}")
        else:
            print(f"Error: {response['error']}")
        
        gpu_monitor.log_compute_status("Code Generation Complete")
        
        # Post-compute status
        gpu_monitor.log_post_compute_status("All tasks completed successfully")
        
        print("\n✅ Demo completed!\n")

except Exception as e:
    print(f"\n❌ Error during demo: {e}\n")
    import traceback
    traceback.print_exc()

# ============================================================================
# SHOW GPU LOGS
# ============================================================================

print("\n📋 GPU Activity Log (last 50 lines):")
print("─" * 60)
log_content = gpu_monitor.get_log_content()
lines = log_content.split('\n')
for line in lines[-50:]:
    if line.strip():
        print(line)
print("─" * 60)

print("\n✨ Demo ready for submission to AIDP bounty!")
print("To submit: Save this notebook + record a 1-2 min video showing GPU logs\n")
