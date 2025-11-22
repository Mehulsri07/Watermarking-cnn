"""
Quick script to download sample images for training and testing
Uses Lorem Picsum for random sample images
"""
import urllib.request
import os
import sys

def download_samples(num_train=80, num_test=20):
    """
    Download sample images from Lorem Picsum
    
    Args:
        num_train: Number of training images to download
        num_test: Number of test images to download
    """
    # Create directories
    os.makedirs('train_images', exist_ok=True)
    os.makedirs('test_images', exist_ok=True)
    
    print("="*60)
    print("DOWNLOADING SAMPLE IMAGES")
    print("="*60)
    
    # Download training images
    print(f"\n📥 Downloading {num_train} training images...")
    for i in range(num_train):
        try:
            url = f"https://picsum.photos/256/256?random={i}"
            filepath = f"train_images/train_{i:03d}.jpg"
            urllib.request.urlretrieve(url, filepath)
            if (i+1) % 5 == 0:
                print(f"  ✓ Downloaded {i+1}/{num_train}")
        except Exception as e:
            print(f"  ✗ Error downloading train image {i}: {e}")
    
    # Download test images
    print(f"\n📥 Downloading {num_test} test images...")
    for i in range(num_test):
        try:
            url = f"https://picsum.photos/256/256?random={100+i}"
            filepath = f"test_images/test_{i:03d}.jpg"
            urllib.request.urlretrieve(url, filepath)
            print(f"  ✓ Downloaded {i+1}/{num_test}")
        except Exception as e:
            print(f"  ✗ Error downloading test image {i}: {e}")
    
    print("\n" + "="*60)
    print(f"✓ COMPLETE! Downloaded {num_train} training + {num_test} test images")
    print("="*60)
    print("\nNext step: Run 'python train_and_evaluate.py'")

if __name__ == "__main__":
    # Parse command line arguments
    num_train = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    num_test = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    print(f"\nConfiguration:")
    print(f"  Training images: {num_train}")
    print(f"  Test images: {num_test}")
    print(f"\nTip: Use more images for better results!")
    print(f"Example: python download_samples.py 50 10\n")
    
    download_samples(num_train, num_test)
