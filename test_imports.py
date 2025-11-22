"""
Test script to verify all imports work correctly
Run this before training to check setup
"""
import sys
import os

print("="*70)
print("IMPORT TEST")
print("="*70)

# Add paths
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

print(f"\nCurrent directory: {os.getcwd()}")
print(f"Script directory: {script_dir}")
print(f"\nPython path (first 3):")
for i, path in enumerate(sys.path[:3], 1):
    print(f"  {i}. {path}")

print("\n" + "-"*70)
print("Testing imports...")
print("-"*70)

tests = []

# Test 1: Basic imports
try:
    import tensorflow as tf
    import numpy as np
    print("✓ TensorFlow and NumPy")
    tests.append(True)
except Exception as e:
    print(f"✗ TensorFlow/NumPy: {e}")
    tests.append(False)

# Test 2: Config
try:
    from configs import *
    print("✓ configs")
    tests.append(True)
except Exception as e:
    print(f"✗ configs: {e}")
    tests.append(False)

# Test 3: Models
try:
    from models.wavetf_model import WaveTFModel
    print("✓ models.wavetf_model")
    tests.append(True)
except Exception as e:
    print(f"✗ models.wavetf_model: {e}")
    tests.append(False)

# Test 4: Data loaders
try:
    from data_loaders.merged_data_loader import MergedDataLoader
    print("✓ data_loaders.merged_data_loader")
    tests.append(True)
except Exception as e:
    print(f"✗ data_loaders.merged_data_loader: {e}")
    tests.append(False)

# Test 5: Utils
try:
    from utils.metrics import calculate_psnr, calculate_ssim, calculate_ber
    print("✓ utils.metrics")
    tests.append(True)
except Exception as e:
    print(f"✗ utils.metrics: {e}")
    tests.append(False)

# Test 6: Attacks
try:
    from attacks.gaussian_noise_attack import GaussianNoiseAttack
    print("✓ attacks.gaussian_noise_attack")
    tests.append(True)
except Exception as e:
    print(f"✗ attacks.gaussian_noise_attack: {e}")
    tests.append(False)

print("\n" + "="*70)
if all(tests):
    print("✅ ALL IMPORTS SUCCESSFUL!")
    print("\nYou can now run: python train_and_evaluate.py")
else:
    print("❌ SOME IMPORTS FAILED")
    print("\nTroubleshooting:")
    print("1. Make sure you're in the Watermarking-cnn directory")
    print("2. Check that all __init__.py files exist")
    print("3. Verify directory structure is intact")
    print("\nRun: python verify_setup.py")
print("="*70)

sys.exit(0 if all(tests) else 1)
