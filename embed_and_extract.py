"""
Simple script to embed and extract watermarks from images
"""
import tensorflow as tf
import numpy as np
import cv2
import os
from configs import *
from models.wavetf_model import WaveTFModel
from utils.metrics import calculate_psnr, calculate_ssim, calculate_ber

def load_model(weights_path):
    """Load trained model"""
    print(f"Loading model from: {weights_path}")
    model = WaveTFModel(image_size=IMAGE_SIZE, watermark_size=WATERMARK_SIZE).get_model()
    model.load_weights(weights_path)
    print("Model loaded successfully!")
    return model

def load_image(image_path):
    """Load and preprocess image"""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    img = cv2.resize(img, (IMAGE_SIZE[0], IMAGE_SIZE[1]))
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=-1)
    return img

def save_image(image, save_path):
    """Save image"""
    img = (image.squeeze() * 255).astype(np.uint8)
    cv2.imwrite(save_path, img)
    print(f"Saved: {save_path}")

def embed_watermark(model, image, watermark, attack_id=0):
    """
    Embed watermark into image
    
    Args:
        model: Trained model
        image: Input image (256x256x1)
        watermark: Watermark bits (256,)
        attack_id: Attack to simulate (0=no attack)
    
    Returns:
        watermarked_image, extracted_watermark
    """
    image_batch = np.expand_dims(image, axis=0)
    watermark_batch = np.expand_dims(watermark, axis=0)
    attack_id_batch = np.array([[attack_id]], dtype=np.int32)
    
    watermarked_image, extracted_watermark = model.predict(
        [image_batch, watermark_batch, attack_id_batch],
        verbose=0
    )
    
    return watermarked_image[0], extracted_watermark[0]

def main():
    print("="*80)
    print("WATERMARK EMBEDDING & EXTRACTION")
    print("="*80)
    
    # Load model
    model_path = os.path.join(MODEL_OUTPUT_PATH, 'final_model_weights.h5')
    if not os.path.exists(model_path):
        print(f"\nError: Model not found at {model_path}")
        print("Please train the model first!")
        return
    
    model = load_model(model_path)
    
    # Load test image
    test_images = [f for f in os.listdir(TEST_IMAGES_PATH) if f.endswith(('.jpg', '.png'))]
    if not test_images:
        print(f"\nError: No test images found in {TEST_IMAGES_PATH}")
        return
    
    image_path = os.path.join(TEST_IMAGES_PATH, test_images[0])
    print(f"\nLoading image: {image_path}")
    image = load_image(image_path)
    
    # Generate random watermark
    watermark = np.random.randint(0, 2, size=WATERMARK_SIZE).astype(np.float32)
    print(f"Generated watermark: {watermark[:10]}... (showing first 10 bits)")
    
    # Test different attacks
    attacks = [
        (0, "No Attack"),
        (1, "Combined Attack (2-3 random)"),
        (2, "Gaussian Noise"),
        (3, "JPEG Compression"),
        (4, "Cropping"),
        (5, "Scaling")
    ]
    
    output_dir = os.path.join(MODEL_OUTPUT_PATH, 'demo_output')
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*80)
    print("TESTING ALL ATTACKS")
    print("="*80)
    
    for attack_id, attack_name in attacks:
        print(f"\n{attack_name}:")
        
        # Embed and extract
        watermarked_image, extracted_watermark = embed_watermark(model, image, watermark, attack_id)
        
        # Calculate metrics
        psnr = calculate_psnr(np.expand_dims(image, 0), np.expand_dims(watermarked_image, 0))
        ssim = calculate_ssim(np.expand_dims(image, 0), np.expand_dims(watermarked_image, 0))
        ber = calculate_ber(watermark, extracted_watermark)
        
        print(f"  PSNR: {psnr:.2f} dB")
        print(f"  SSIM: {ssim:.4f}")
        print(f"  BER:  {ber:.2f}%")
        
        # Save watermarked image
        safe_name = attack_name.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '')
        save_path = os.path.join(output_dir, f'watermarked_{safe_name}.png')
        save_image(watermarked_image, save_path)
    
    # Save original for comparison
    save_image(image, os.path.join(output_dir, 'original.png'))
    
    print("\n" + "="*80)
    print(f"✓ All results saved to: {output_dir}")
    print("="*80)

if __name__ == "__main__":
    main()
