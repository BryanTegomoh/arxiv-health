#!/bin/bash
# Quick Start Script for arXiv Health Monitor (macOS/Linux)

echo "======================================================================"
echo "arXiv Health Monitor - Quick Start"
echo "======================================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "[ERROR] .env file not found!"
    echo "Please copy .env.example to .env and add your API key:"
    echo "   cp .env.example .env"
    echo "Then edit .env and add your Gemini API key."
    echo ""
    exit 1
fi

echo "[1/3] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[2/3] Running arXiv Health Monitor..."
python run.py

echo ""
echo "[3/3] Opening website..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    open docs/index.html
else
    xdg-open docs/index.html 2>/dev/null || echo "Please open docs/index.html in your browser"
fi

echo ""
echo "======================================================================"
echo "Done! Your website should open in your browser."
echo "======================================================================"
