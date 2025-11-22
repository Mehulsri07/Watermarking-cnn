"""
Setup verification script
Checks if everything is ready for training
"""
import os
import sys

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    required = ['tensorflow', 'numpy', 'cv2', 'matplotlib', 'skimage']
    missing = []
    
    for package in required:
        try:
            if package == 'cv2':
                __import__('cv2')
            elif package == 'skimage':
                __import__('skimage')
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    return True

def check_directories():
    """Check if required directories exist"""
    print("\n📁 Checking directories...")
    dirs = ['train_images', 'test_images', 'models', 'attacks', 'data_loaders', 'utils']
    all_exist = True
    
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - MISSING")
            all_exist = False
    
    return all_exist

def check_images():
    """Check if training and test images exist"""
    print("\n🖼️  Checking images...")
    
    train_images = [f for f in os.listdir('train_images') if f.endswith(('.jpg', '.png', '.jpeg'))] if os.path.exists('train_images') else []
    test_images = [f for f in os.listdir('test_images') if f.endswith(('.jpg', '.png', '.jpeg'))] if os.path.exists('test_images') else []
    
    print(f"  Training images: {len(train_images)}")
    print(f"  Test images: {len(test_images)}")
    
    if len(train_images) == 0:
        print("\n  ⚠️  No training images found!")
        print("  Run: python download_samples.py")
        return False
    
    if len(test_images) == 0:
        print("\n  ⚠️  No test images found!")
        print("  Run: python download_samples.py")
        return False
    
    if len(train_images) < 10:
        print("\n  ⚠️  Only", len(train_images), "training images (recommend 20+)")
    
    return True

def check_gpu():
    """Check if GPU is available"""
    print("\n🎮 Checking GPU...")
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"  ✓ GPU available: {len(gpus)} device(s)")
            for gpu in gpus:
                print(f"    - {gpu.name}")
            return True
        else:
            print("  ⚠️  No GPU found (will use CPU - slower)")
            return False
    except Exception as e:
        print(f"  ✗ Error checking GPU: {e}")
        return False

def main():
    print("="*60)
    print("WATERMARK CNN - SETUP VERIFICATION")
    print("="*60)
    
    checks = {
        'Dependencies': check_dependencies(),
        'Directories': check_directories(),
        'Images': check_images(),
        'GPU': check_gpu()
    }
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for check_name, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check_name:20s} {status}")
    
    all_passed = all(checks.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("="*60)
        print("\nYou're ready to train!")
        print("Run: python train_and_evaluate.py")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print("="*60)
        print("\nPlease fix the issues above before training.")
        print("\nQuick fixes:")
        print("  - Missing packages: pip install -r requirements.txt")
        print("  - Missing images: python download_samples.py")
        print("  - No GPU: Use Google Colab for free GPU")
    
    print("\n" + "="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
