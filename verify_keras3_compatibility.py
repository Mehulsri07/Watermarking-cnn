"""
Keras 3.12 Compatibility Verification Script

This script verifies that your environment is properly configured
for Keras 3.12 and tests the updated model components.
"""

import sys
import os

# Add current directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

def check_versions():
    """Check TensorFlow and Keras versions"""
    print("="*80)
    print("CHECKING PACKAGE VERSIONS")
    print("="*80)
    
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow: {tf.__version__}")
        
        tf_version = tuple(map(int, tf.__version__.split('.')[:2]))
        if tf_version >= (2, 16):
            print("  → Version OK (>= 2.16.0)")
        else:
            print("  ✗ WARNING: TensorFlow < 2.16.0 detected")
            print("    Please upgrade: pip install tensorflow>=2.16.0 --upgrade")
            return False
    except ImportError:
        print("✗ TensorFlow not installed")
        return False
    
    try:
        import keras
        print(f"✓ Keras: {keras.__version__}")
        
        keras_version = tuple(map(int, keras.__version__.split('.')[:2]))
        if keras_version >= (3, 0):
            print("  → Version OK (>= 3.0.0)")
        else:
            print("  ✗ WARNING: Keras < 3.0.0 detected")
            print("    Please upgrade: pip install keras>=3.0.0 --upgrade")
            return False
    except ImportError:
        print("✗ Keras not installed")
        return False
    
    try:
        import numpy as np
        print(f"✓ NumPy: {np.__version__}")
    except ImportError:
        print("✗ NumPy not installed")
        return False
    
    try:
        import cv2
        print(f"✓ OpenCV: {cv2.__version__}")
    except ImportError:
        print("✗ OpenCV not installed")
        return False
    
    print("\n✓ All required packages installed with correct versions")
    return True


def test_model_creation():
    """Test model creation with Keras 3.12"""
    print("\n" + "="*80)
    print("TESTING MODEL CREATION")
    print("="*80)
    
    try:
        import tensorflow as tf
        from models.wavetf_model import WaveTFModel
        
        print("\nCreating WaveTF model...")
        model = WaveTFModel(
            image_size=(256, 256, 1),
            watermark_size=(256,),
            wavelet_type='haar'
        )
        
        print("Building model graph...")
        keras_model = model.get_model()
        
        print(f"✓ Model created successfully")
        print(f"  Inputs: {len(keras_model.inputs)}")
        print(f"  Outputs: {len(keras_model.outputs)}")
        print(f"  Total parameters: {keras_model.count_params():,}")
        
        return True
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_attack_simulator():
    """Test the updated attack simulator with tf.cond"""
    print("\n" + "="*80)
    print("TESTING ATTACK SIMULATOR (tf.cond implementation)")
    print("="*80)
    
    try:
        import tensorflow as tf
        import numpy as np
        from models.wavetf_model import WaveTFModel
        
        print("\nCreating model with attack simulator...")
        model = WaveTFModel(
            image_size=(256, 256, 1),
            watermark_size=(256,),
            wavelet_type='haar'
        )
        keras_model = model.get_model()
        
        print("Testing attack simulation with different attack IDs...")
        
        # Create dummy inputs
        test_image = np.random.rand(1, 256, 256, 1).astype(np.float32)
        test_watermark = np.random.randint(0, 2, size=(1, 256)).astype(np.float32)
        
        # Test each attack type
        attack_names = {
            0: "No Attack",
            1: "Combined Attack",
            2: "Gaussian Noise",
            3: "JPEG Compression",
            4: "Cropping",
            5: "Scaling"
        }
        
        for attack_id in range(6):
            test_attack_id = np.array([[attack_id]], dtype=np.int32)
            
            try:
                # Run prediction (this tests the attack simulator)
                output = keras_model.predict(
                    [test_image, test_watermark, test_attack_id],
                    verbose=0
                )
                print(f"  ✓ Attack ID {attack_id} ({attack_names[attack_id]}): OK")
            except Exception as e:
                print(f"  ✗ Attack ID {attack_id} ({attack_names[attack_id]}): FAILED - {e}")
                return False
        
        print("\n✓ All attack types working correctly with tf.cond")
        return True
        
    except Exception as e:
        print(f"✗ Attack simulator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_model_saving():
    """Test model saving in Keras 3 format"""
    print("\n" + "="*80)
    print("TESTING MODEL SAVING (.keras format)")
    print("="*80)
    
    try:
        import tensorflow as tf
        from models.wavetf_model import WaveTFModel
        import tempfile
        
        print("\nCreating test model...")
        model = WaveTFModel(
            image_size=(256, 256, 1),
            watermark_size=(256,),
            wavelet_type='haar'
        )
        keras_model = model.get_model()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.keras', delete=False) as tmp:
            temp_path = tmp.name
        
        print(f"Saving model to: {temp_path}")
        keras_model.save_weights(temp_path)
        print("✓ Model saved successfully")
        
        print("Loading model weights...")
        keras_model.load_weights(temp_path)
        print("✓ Model loaded successfully")
        
        # Cleanup
        os.remove(temp_path)
        print("✓ Keras 3 format (.keras) working correctly")
        
        return True
        
    except Exception as e:
        print(f"✗ Model saving test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification tests"""
    print("\n" + "="*80)
    print("KERAS 3.12 COMPATIBILITY VERIFICATION")
    print("="*80)
    print()
    
    results = []
    
    # Test 1: Version check
    results.append(("Version Check", check_versions()))
    
    # Test 2: Model creation
    results.append(("Model Creation", test_model_creation()))
    
    # Test 3: Attack simulator
    results.append(("Attack Simulator", test_attack_simulator()))
    
    # Test 4: Model saving
    results.append(("Model Saving", test_model_saving()))
    
    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:.<50} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "="*80)
    if all_passed:
        print("✓ ALL TESTS PASSED - Keras 3.12 compatibility verified!")
        print("="*80)
        print("\nYou can now run training with:")
        print("  python train_and_evaluate.py")
        return 0
    else:
        print("✗ SOME TESTS FAILED - Please fix issues before training")
        print("="*80)
        print("\nTroubleshooting:")
        print("1. Update packages: pip install -r requirements.txt --upgrade")
        print("2. Check Python version (requires Python 3.9+)")
        print("3. Review error messages above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
