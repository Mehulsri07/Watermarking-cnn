"""
Evaluation metrics for watermarking system
Calculates PSNR, SSIM, and BER
"""
import tensorflow as tf
import numpy as np
from tensorflow.image import ssim as tf_ssim


def calculate_psnr(original, watermarked):
    """
    Calculate Peak Signal-to-Noise Ratio (PSNR)
    
    Args:
        original: Original image tensor
        watermarked: Watermarked image tensor
        
    Returns:
        PSNR value in dB (higher is better, >30 dB is good, >35 dB is excellent)
    """
    # Ensure images are in [0, 1] range
    original = tf.cast(original, tf.float32)
    watermarked = tf.cast(watermarked, tf.float32)
    
    # Calculate MSE
    mse = tf.reduce_mean(tf.square(original - watermarked))
    
    # Avoid division by zero
    if mse == 0:
        return float('inf')
    
    # Calculate PSNR
    max_pixel = 1.0  # Assuming normalized images
    psnr = 20 * tf.math.log(max_pixel / tf.sqrt(mse)) / tf.math.log(10.0)
    
    return psnr.numpy()


def calculate_ssim(original, watermarked):
    """
    Calculate Structural Similarity Index (SSIM)
    
    Args:
        original: Original image tensor
        watermarked: Watermarked image tensor
        
    Returns:
        SSIM value between 0 and 1 (higher is better, >0.95 is good)
    """
    # Ensure images are in [0, 1] range
    original = tf.cast(original, tf.float32)
    watermarked = tf.cast(watermarked, tf.float32)
    
    # Calculate SSIM
    ssim_value = tf_ssim(original, watermarked, max_val=1.0)
    
    return tf.reduce_mean(ssim_value).numpy()


def calculate_ber(original_watermark, extracted_watermark, threshold=0.5):
    """
    Calculate Bit Error Rate (BER)
    
    Args:
        original_watermark: Original watermark bits (0 or 1)
        extracted_watermark: Extracted watermark bits (probabilities or 0/1)
        threshold: Threshold for converting probabilities to bits
        
    Returns:
        BER as percentage (lower is better, <5% is good)
    """
    # Convert to numpy if tensors
    if isinstance(original_watermark, tf.Tensor):
        original_watermark = original_watermark.numpy()
    if isinstance(extracted_watermark, tf.Tensor):
        extracted_watermark = extracted_watermark.numpy()
    
    # Flatten arrays
    original_watermark = original_watermark.flatten()
    extracted_watermark = extracted_watermark.flatten()
    
    # Convert extracted watermark probabilities to binary
    extracted_binary = (extracted_watermark > threshold).astype(np.float32)
    
    # Calculate bit errors
    bit_errors = np.sum(np.abs(original_watermark - extracted_binary))
    total_bits = len(original_watermark)
    
    # Calculate BER as percentage
    ber = (bit_errors / total_bits) * 100
    
    return ber


def calculate_all_metrics(original_image, watermarked_image, original_watermark, extracted_watermark):
    """
    Calculate all metrics at once
    
    Returns:
        Dictionary with PSNR, SSIM, and BER
    """
    metrics = {
        'psnr': calculate_psnr(original_image, watermarked_image),
        'ssim': calculate_ssim(original_image, watermarked_image),
        'ber': calculate_ber(original_watermark, extracted_watermark)
    }
    
    return metrics


def evaluate_quality(psnr, ssim, ber):
    """
    Evaluate overall quality based on metrics
    
    Returns:
        Quality rating: 'Excellent', 'Good', 'Fair', 'Poor'
    """
    if psnr > 38 and ssim > 0.96 and ber < 3:
        return 'Excellent'
    elif psnr > 35 and ssim > 0.94 and ber < 5:
        return 'Good'
    elif psnr > 30 and ssim > 0.90 and ber < 10:
        return 'Fair'
    else:
        return 'Poor'


def print_metrics(metrics, attack_name="Unknown"):
    """
    Pretty print metrics
    """
    print(f"\n{'='*60}")
    print(f"Metrics for: {attack_name}")
    print(f"{'='*60}")
    print(f"PSNR: {metrics['psnr']:.2f} dB")
    print(f"SSIM: {metrics['ssim']:.4f}")
    print(f"BER:  {metrics['ber']:.2f}%")
    
    quality = evaluate_quality(metrics['psnr'], metrics['ssim'], metrics['ber'])
    print(f"Quality: {quality}")
    print(f"{'='*60}\n")
