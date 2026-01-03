"""GPU Monitor for AIDP Decentralized Compute

Monitors GPU utilization and logs metrics during AI inference tasks.
"""

import subprocess
import json
from datetime import datetime
from typing import Dict, Optional
import os


class GPUMonitor:
    """Monitors GPU status using nvidia-smi"""
    
    def __init__(self, log_file: str = "gpu-usage.log"):
        self.log_file = log_file
        self.is_available = self._check_gpu_availability()
        self.logs = []
    
    def _check_gpu_availability(self) -> bool:
        """Check if nvidia-smi is available"""
        try:
            subprocess.run(['nvidia-smi', '--version'], 
                         capture_output=True, check=True, timeout=5)
            return True
        except Exception as e:
            print(f'[GPUMonitor] NVIDIA GPU tools not available: {e}')
            return False
    
    def _run_nvidia_smi(self, query: str) -> str:
        """Run nvidia-smi with custom query"""
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
        """Log GPU status before compute task"""
        timestamp = datetime.now().isoformat()
        separator = "=" * 60
        
        log_entry = f"\n{separator}\n[{timestamp}] PRE-COMPUTE GPU STATUS: {task_name}\n{separator}\n"
        
        if self.is_available:
            try:
                # GPU Details
                gpu_details = self._run_nvidia_smi("index,name,driver_version,memory.total")
                log_entry += f"GPU Details:\n{gpu_details}\n"
                
                # Memory and utilization
                metrics = self._run_nvidia_smi("index,memory.used,memory.free,utilization.gpu,temperature.gpu")
                log_entry += f"\nMemory & Utilization:\n{metrics}\n"
                
            except Exception as e:
                log_entry += f"Error querying GPU: {e}\n"
        else:
            log_entry += "GPU not available - CPU mode\n"
        
        self._append_log(log_entry)
        print(log_entry)
    
    def log_compute_status(self, task_name: str = "Processing"):
        """Log GPU status during compute task"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] DURING: {task_name}\n"
        
        if self.is_available:
            try:
                metrics = self._run_nvidia_smi("index,utilization.gpu,utilization.memory,memory.used,temperature.gpu")
                log_entry += metrics + "\n"
            except Exception as e:
                log_entry += f"Error: {e}\n"
        
        self._append_log(log_entry)
        print(log_entry)
    
    def log_post_compute_status(self, summary: str = ""):
        """Log GPU status after compute task"""
        timestamp = datetime.now().isoformat()
        separator = "=" * 60
        
        log_entry = f"\n{separator}\n[{timestamp}] POST-COMPUTE GPU STATUS\n{separator}\n"
        
        if self.is_available:
            try:
                metrics = self._run_nvidia_smi("index,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu")
                log_entry += f"Final GPU State:\n{metrics}\n"
            except Exception as e:
                log_entry += f"Error: {e}\n"
        
        if summary:
            log_entry += f"\nResult: {summary}\n"
        
        log_entry += f"{separator}\n\n"
        self._append_log(log_entry)
        print(log_entry)
    
    def get_summary(self) -> Dict:
        """Get GPU summary info"""
        if not self.is_available:
            return {
                "status": "unavailable",
                "mode": "cpu"
            }
        
        try:
            gpu_info = self._run_nvidia_smi("name,driver_version,memory.total")
            lines = gpu_info.split('\n')
            if lines:
                parts = lines[0].split(', ')
                return {
                    "status": "available",
                    "mode": "gpu",
                    "gpu": parts[0] if len(parts) > 0 else "Unknown",
                    "driver": parts[1] if len(parts) > 1 else "Unknown",
                    "memory": parts[2] if len(parts) > 2 else "Unknown",
                    "log_file": self.log_file
                }
        except Exception as e:
            return {"status": "error", "error": str(e)}
        
        return {"status": "error", "error": "Unknown error"}
    
    def get_log_content(self) -> str:
        """Get log file content"""
        try:
            with open(self.log_file, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading log: {e}\n" + "\n".join(self.logs)
    
    def _append_log(self, message: str):
        """Append message to log"""
        self.logs.append(message)
        try:
            with open(self.log_file, 'a') as f:
                f.write(message)
        except Exception as e:
            print(f"[GPUMonitor] Failed to write log: {e}")
    
    def clear_log(self):
        """Clear log file"""
        try:
            with open(self.log_file, 'w') as f:
                f.write("")
            self.logs = []
            print(f"[GPUMonitor] Log cleared: {self.log_file}")
        except Exception as e:
            print(f"[GPUMonitor] Failed to clear log: {e}")
