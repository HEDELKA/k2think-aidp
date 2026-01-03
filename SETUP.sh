#!/bin/bash
# Quick setup script for K2Think AIDP demo

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   K2Think AIDP GPU Compute - Setup                         ║"
echo "║   Custom AI Agent Wrapper for Decentralized Compute        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python..."
python_version=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✓ $python_version"
else
    echo "❌ Python 3 not found. Install Python 3.8+:"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   macOS: brew install python3"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create .env
echo ""
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your K2Think credentials:"
    echo "   - K2THINK_EMAIL=your-email@example.com"
    echo "   - K2THINK_PASSWORD=your-password"
    echo ""
    echo "   Then run: python colab_demo.py"
else
    echo "✓ .env file exists"
fi

# Check GPU
echo ""
echo "🎮 GPU Check..."
if command -v nvidia-smi &> /dev/null; then
    gpu_info=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | head -1)
    echo "✓ GPU detected: $gpu_info"
else
    echo "⚠️  GPU not detected (CPU mode will be used)"
    echo "   To enable GPU:"
    echo "   - Install NVIDIA drivers: https://www.nvidia.com/Download/driverDetails.aspx"
    echo "   - Or use Google Colab: https://colab.research.google.com"
fi

# Done
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   ✓ Setup Complete!                                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your K2Think credentials"
echo "  2. Run: python colab_demo.py"
echo "  3. Or use Google Colab (recommended):"
echo "     https://colab.research.google.com/github/HEDELKA/k2think-aidp/blob/python-colab/colab_demo.ipynb"
echo ""
