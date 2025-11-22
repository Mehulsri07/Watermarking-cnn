#!/bin/bash
# Script to push changes to GitHub

echo "============================================================"
echo "PUSH TO GITHUB"
echo "============================================================"
echo ""

echo "Step 1: Adding all changes..."
git add .
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to add files"
    exit 1
fi
echo "Done!"
echo ""

echo "Step 2: Committing changes..."
git commit -m "Update: Fixed imports, updated references to Watermarking-cnn, optimized for Colab"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to commit"
    exit 1
fi
echo "Done!"
echo ""

echo "Step 3: Pushing to GitHub..."
git push origin main
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to push"
    echo ""
    echo "If this is your first push, you may need to set the remote:"
    echo "  git remote add origin https://github.com/Mehulsri07/Watermarking-cnn.git"
    echo "  git push -u origin main"
    exit 1
fi
echo "Done!"
echo ""

echo "============================================================"
echo "SUCCESS! Changes pushed to GitHub"
echo "============================================================"
echo ""
echo "Your repository: https://github.com/Mehulsri07/Watermarking-cnn"
echo "Colab notebook: https://colab.research.google.com/github/Mehulsri07/Watermarking-cnn/blob/main/watermark_colab.ipynb"
echo ""
