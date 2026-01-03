const { execSync } = require('child_process');
const fs = require('fs');

class GPUMonitor {
  constructor(logFile = 'gpu-usage.log') {
    this.logFile = logFile;
    this.isAvailable = this.checkGPUAvailability();
  }

  checkGPUAvailability() {
    try {
      execSync('nvidia-smi --version', { stdio: 'ignore' });
      return true;
    } catch (error) {
      console.warn('[GPUMonitor] NVIDIA GPU tools not available');
      return false;
    }
  }

  logPreComputeStatus() {
    const timestamp = new Date().toISOString();
    const separator = '='.repeat(60);
    let log = `\n${separator}\n[${timestamp}] PRE-COMPUTE GPU STATUS\n${separator}\n`;

    if (this.isAvailable) {
      try {
        const gpuStatus = execSync(
          'nvidia-smi --query-gpu=index,name,driver_version --format=csv,noheader',
          { encoding: 'utf-8' }
        );
        log += 'GPU Details:\n' + gpuStatus + '\n';

        const gpuMetrics = execSync(
          'nvidia-smi --query-gpu=index,memory.total,memory.used,utilization.gpu,temperature.gpu --format=csv,noheader',
          { encoding: 'utf-8' }
        );
        log += 'Memory & Utilization:\n' + gpuMetrics + '\n';
      } catch (error) {
        log += `Error: ${error.message}\n`;
      }
    } else {
      log += 'GPU not available - CPU mode\n';
    }

    this.appendLog(log);
    console.log(log);
  }

  logComputeStatus(taskName = 'AI Inference') {
    const timestamp = new Date().toISOString();
    let log = `[${timestamp}] COMPUTE: ${taskName}\n`;

    if (this.isAvailable) {
      try {
        const gpuMetrics = execSync(
          'nvidia-smi --query-gpu=index,utilization.gpu,utilization.memory,memory.used --format=csv,noheader',
          { encoding: 'utf-8' }
        );
        log += gpuMetrics;
      } catch (error) {
        log += `Error: ${error.message}\n`;
      }
    }

    this.appendLog(log);
    console.log(log);
  }

  logPostComputeStatus() {
    const timestamp = new Date().toISOString();
    const separator = '='.repeat(60);
    let log = `\n${separator}\n[${timestamp}] POST-COMPUTE GPU STATUS\n${separator}\n`;

    if (this.isAvailable) {
      try {
        const gpuMetrics = execSync(
          'nvidia-smi --query-gpu=index,memory.total,memory.used,utilization.gpu --format=csv,noheader',
          { encoding: 'utf-8' }
        );
        log += 'Final GPU State:\n' + gpuMetrics + '\n';
      } catch (error) {
        log += `Error: ${error.message}\n`;
      }
    }

    log += `${separator}\n\n`;
    this.appendLog(log);
    console.log(log);
  }

  appendLog(message) {
    try {
      fs.appendFileSync(this.logFile, message);
    } catch (error) {
      console.error(`Failed to write log: ${error.message}`);
    }
  }

  getSummary() {
    if (!this.isAvailable) {
      return { status: 'unavailable', mode: 'cpu' };
    }

    try {
      const gpuInfo = execSync(
        'nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader',
        { encoding: 'utf-8' }
      ).trim();

      const [gpuName, driver, memory] = gpuInfo.split(', ');

      return {
        status: 'available',
        mode: 'gpu',
        gpu: gpuName,
        driver,
        memory,
        logFile: this.logFile
      };
    } catch (error) {
      return { status: 'error', error: error.message };
    }
  }

  getLogContent() {
    try {
      return fs.readFileSync(this.logFile, 'utf-8');
    } catch (error) {
      return `Error reading log: ${error.message}`;
    }
  }
}

module.exports = GPUMonitor;
