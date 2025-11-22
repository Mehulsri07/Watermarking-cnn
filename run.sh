#!/bin/bash
# Quick run script for Linux/Mac
# This script verifies setup and runs training

echo "============================================================"
echo "WATERMARK CNN - QUICK RUN SCRIPT"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Step 1: Verifying setup..."
echo ""
python3 verify_setup.py
if [ $? -ne 0 ]; then
    echo ""
    echo "Setup verification failed. Please fix the issues above."
    exit 1
fi

echo ""
echo "============================================================"
echo "Step 2: Starting training and evaluation..."
echo "============================================================"
echo ""
python3 train_and_evaluate.py

echo ""
echo "============================================================"
echo "COMPLETE!"
echo "============================================================"
echo ""
echo "Results saved to: config_1_baseline/evaluation_results/"
echo ""
