# K2Think AIDP GPU Compute Agent - Python Version

**Custom AI Agent Wrapper optimized for Decentralized Compute**

Python implementation with Google Colab support. Run GPU-accelerated AI on free cloud GPU with real-time monitoring.

## 🚀 Quick Start (Google Colab - Recommended!)

### Option 1: Direct Colab Link

Click to open in Google Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/HEDELKA/k2think-aidp/blob/python-colab/colab_demo.ipynb)

### Option 2: Manual Setup in Colab

1. Open Google Colab: https://colab.research.google.com
2. `File` → `Open notebook` → `GitHub` tab
3. Paste: `HEDELKA/k2think-aidp`
4. Select `colab_demo.ipynb` from `python-colab` branch
5. **Important**: Go to `Runtime` → `Change runtime type` → Select **GPU**
6. Run all cells!

## 🎯 Features

- ✅ **Python 3** - Simple, readable code
- ✅ **Google Colab** - Free GPU, no setup needed
- ✅ **GPU Monitoring** - Real-time nvidia-smi logging
- ✅ **K2Think API** - OpenAI-compatible interface
- ✅ **Zero Docker** - Run directly in notebook

## 📊 What Happens

1. **Startup** → Detect GPU and log device info
2. **API Call** → Send request to K2Think
3. **Inference** → Model runs on GPU
4. **Logging** → Track GPU metrics before/during/after
5. **Results** → Display AI response + GPU stats

## 🔧 Files

| File | Purpose |
|------|---------|
| `colab_demo.ipynb` | **Use this!** Jupyter notebook for Colab |
| `colab_demo.py` | Standalone Python script |
| `gpu_monitor.py` | GPU monitoring module |
| `k2think_client.py` | K2Think API client |
| `requirements.txt` | Python dependencies |

## 📝 K2Think Credentials

You need K2Think account credentials:

### In Google Colab:

**Option A: Input in Notebook**
- The notebook will ask for email/password
- Use `getpass()` for secure input
- Never shows password on screen

**Option B: Environment Variables**
```
# In Colab, before running:
import os
os.environ['K2THINK_EMAIL'] = 'your-email@example.com'
os.environ['K2THINK_PASSWORD'] = 'your-password'
```

**Option C: .env File (local)**
```bash
cp .env.example .env
# Edit .env with your credentials
```

## 🎬 Running the Demo

### In Google Colab (Recommended)

1. **Enable GPU**
   - Runtime → Change runtime type → GPU → Save

2. **Run All Cells**
   - Ctrl+F9 (Windows) or Cmd+F9 (Mac)
   - Or click "Run all" button

3. **Watch the Magic**
   - GPU status printed
   - AI responses generated
   - GPU metrics logged

### Locally (Python)

```bash
# Install dependencies
pip install -r requirements.txt

# Run demo script
python colab_demo.py

# Or use as library:
python
>>> from k2think_client import K2ThinkClient
>>> client = K2ThinkClient(email='...', password='...')
>>> response = client.simple_ask("Hello!")
>>> print(response)
```

## 📊 GPU Logs

The demo generates GPU activity logs showing:

```
============================================================
[2024-01-03T14:23:45.123Z] PRE-COMPUTE GPU STATUS: K2Think AI Inference
============================================================
GPU Details:
0, NVIDIA A100-SXM4-40GB, 535.104.05, 40960 MB

Memory & Utilization:
0, 0 MB, 40960 MB, 0 %, 35°C

[2024-01-03T14:23:46.234Z] DURING: Text Generation
0, 85 %, 75 %, 18432 MB, 72°C
```

**Perfect for demo video!**

## 🎥 Recording Demo Video (1-2 min)

### In Google Colab:

1. **Full Cell Output**
   - All GPU logs visible in output
   - Shows ai responses
   - Professional looking

2. **How to Record:**
   ```
   Option A: Screenshot
   - Scroll through the output
   - Take screen capture with GPU metrics visible
   
   Option B: Screen Recording
   - Use OBS Studio or built-in screen recorder
   - Record while notebook runs
   - Capture GPU logs + responses
   ```

3. **Upload to YouTube**
   - Make it public or unlisted
   - Use title: "K2Think AIDP GPU Compute Demo"
   - Include link in submission

## 📋 Submission Checklist

- [ ] Opened colab_demo.ipynb in Colab
- [ ] Enabled GPU in Runtime settings
- [ ] Entered K2Think credentials
- [ ] Ran all cells successfully
- [ ] GPU logs printed
- [ ] Recorded 1-2 min demo video
- [ ] Uploaded video to YouTube (public)
- [ ] Have notebook link
- [ ] Ready to submit to Superteam Earn

## 🔗 AIDP Submission Links

### Main Repository
https://github.com/HEDELKA/k2think-aidp

### Colab Notebook
https://colab.research.google.com/github/HEDELKA/k2think-aidp/blob/python-colab/colab_demo.ipynb

### GitHub (Python Branch)
https://github.com/HEDELKA/k2think-aidp/tree/python-colab

## 🚀 AIDP Network

- **Website**: https://aidp.store
- **Telegram**: https://t.me/Aidpofficial
- **Bounty**: AIDP GPU Compute & Recruit Campaign
- **Prize**: 350 USDC (1st place)

## 🛠️ Troubleshooting

### "GPU not available"
- Go to `Runtime` → `Change runtime type`
- Select **GPU** as Hardware accelerator
- Click `Save`
- Run cells again

### "Authentication failed"
- Double-check email and password
- Verify you can login at https://www.k2think.ai
- No special characters should need escaping

### "API Error"
- K2Think service might be temporarily down
- Try again after 1-2 minutes
- Check K2Think status page

### "Timeout"
- Increase `timeout=30` in k2think_client.py
- Or reduce `max_tokens` in chat_completion call

## 📚 Documentation

- [Main README](README.md) - Docker & full setup
- [GPU Monitor Code](gpu_monitor.py) - Implementation details
- [K2Think Client](k2think_client.py) - API reference

## 💡 Tips

1. **GPU Memory** - Free tier Colab has ~15GB GPU memory
2. **Rate Limiting** - Don't spam API calls
3. **Session Duration** - Colab disconnects after ~12 hours
4. **Reproducibility** - Save GPU logs for verification

## ✨ Ready?

Click the Colab button above and run!

**Custom AI Agent Wrapper optimized for Decentralized Compute** 🎮🚀
