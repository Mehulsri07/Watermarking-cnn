"""
Comprehensive model evaluation with metrics, attack tracking, and visualizations
Generates a detailed report with before/after images
"""
import sys
import os

# Add current directory to Python path to fix imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime
from configs import *
from models.wavetf_model import WaveTFModel
from utils.metrics import calculate_psnr, calculate_ssim, calculate_ber, evaluate_quality
import cv2

# Attack names mapping
ATTACK_NAMES = {
    0: "No Attack (Baseline)",
    1: "Combined Attack (2-3 Random)",
    2: "Gaussian Noise",
    3: "JPEG Compression",
    4: "Cropping",
    5: "Scaling",
    6: "Salt & Pepper Noise"
}

class WatermarkEvaluator:
    def __init__(self, model_weights_path):
        """Initialize evaluator with trained model"""
        print("Loading model...")
        self.model = WaveTFModel(image_size=IMAGE_SIZE, watermark_size=WATERMARK_SIZE).get_model()
        self.model.load_weights(model_weights_path)
        print(f"Model loaded from: {model_weights_path}")
        
        # Create output directory for results
        self.output_dir = os.path.join(MODEL_OUTPUT_PATH, 'evaluation_results')
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'images'), exist_ok=True)
        
        self.results = []
    
    def load_test_images(self, num_images=5):
        """Load test images"""
        print(f"\nLoading {num_images} test images from {TEST_IMAGES_PATH}...")
        
        image_files = [f for f in os.listdir(TEST_IMAGES_PATH) if f.endswith(('.jpg', '.png', '.jpeg'))]
        image_files = image_files[:num_images]
        
        images = []
        for img_file in image_files:
            img_path = os.path.join(TEST_IMAGES_PATH, img_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (IMAGE_SIZE[0], IMAGE_SIZE[1]))
            img = img.astype(np.float32) / 255.0
            img = np.expand_dims(img, axis=-1)
            images.append((img, img_file))
        
        print(f"Loaded {len(images)} images")
        return images
    
    def generate_watermark(self):
        """Generate random watermark"""
        return np.random.randint(0, 2, size=WATERMARK_SIZE).astype(np.float32)
    
    def evaluate_single_image(self, image, watermark, attack_id, image_name):
        """Evaluate single image with specific attack"""
        # Prepare inputs
        image_batch = np.expand_dims(image, axis=0)
        watermark_batch = np.expand_dims(watermark, axis=0)
        attack_id_batch = np.array([[attack_id]], dtype=np.int32)
        
        # Get predictions
        watermarked_image, extracted_watermark = self.model.predict(
            [image_batch, watermark_batch, attack_id_batch],
            verbose=0
        )
        
        # Calculate metrics
        psnr = calculate_psnr(image_batch, watermarked_image)
        ssim = calculate_ssim(image_batch, watermarked_image)
        ber = calculate_ber(watermark_batch, extracted_watermark)
        quality = evaluate_quality(psnr, ssim, ber)
        
        result = {
            'image_name': image_name,
            'attack_id': attack_id,
            'attack_name': ATTACK_NAMES[attack_id],
            'psnr': float(psnr),
            'ssim': float(ssim),
            'ber': float(ber),
            'quality': quality,
            'original_image': image,
            'watermarked_image': watermarked_image[0],
            'watermark': watermark,
            'extracted_watermark': extracted_watermark[0]
        }
        
        return result
    
    def visualize_result(self, result, save_path):
        """Create before/after visualization with metrics"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f"Watermarking Evaluation: {result['image_name']}\nAttack: {result['attack_name']}", 
                     fontsize=16, fontweight='bold')
        
        # Original Image
        axes[0, 0].imshow(result['original_image'].squeeze(), cmap='gray')
        axes[0, 0].set_title('Original Image', fontsize=12, fontweight='bold')
        axes[0, 0].axis('off')
        
        # Watermarked Image
        axes[0, 1].imshow(result['watermarked_image'].squeeze(), cmap='gray')
        axes[0, 1].set_title('Watermarked Image (After Attack)', fontsize=12, fontweight='bold')
        axes[0, 1].axis('off')
        
        # Difference (amplified)
        diff = np.abs(result['original_image'] - result['watermarked_image']) * 10
        axes[0, 2].imshow(diff.squeeze(), cmap='hot')
        axes[0, 2].set_title('Difference (10x amplified)', fontsize=12, fontweight='bold')
        axes[0, 2].axis('off')
        
        # Original Watermark
        watermark_img = result['watermark'].reshape(16, 16)
        axes[1, 0].imshow(watermark_img, cmap='gray', interpolation='nearest')
        axes[1, 0].set_title('Original Watermark (16x16)', fontsize=12, fontweight='bold')
        axes[1, 0].axis('off')
        
        # Extracted Watermark
        extracted_img = result['extracted_watermark'].reshape(16, 16)
        axes[1, 1].imshow(extracted_img, cmap='gray', interpolation='nearest')
        axes[1, 1].set_title('Extracted Watermark', fontsize=12, fontweight='bold')
        axes[1, 1].axis('off')
        
        # Metrics Display
        axes[1, 2].axis('off')
        metrics_text = f"""
METRICS:

PSNR: {result['psnr']:.2f} dB
{'✓ Excellent' if result['psnr'] > 38 else '✓ Good' if result['psnr'] > 35 else '○ Fair' if result['psnr'] > 30 else '✗ Poor'}

SSIM: {result['ssim']:.4f}
{'✓ Excellent' if result['ssim'] > 0.96 else '✓ Good' if result['ssim'] > 0.94 else '○ Fair' if result['ssim'] > 0.90 else '✗ Poor'}

BER: {result['ber']:.2f}%
{'✓ Excellent' if result['ber'] < 3 else '✓ Good' if result['ber'] < 5 else '○ Fair' if result['ber'] < 10 else '✗ Poor'}

Overall Quality:
{result['quality']}
        """
        axes[1, 2].text(0.1, 0.5, metrics_text, fontsize=12, verticalalignment='center',
                       family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved visualization: {save_path}")
    
    def evaluate_all_attacks(self, num_images=3):
        """Evaluate all attack types on test images"""
        print("\n" + "="*80)
        print("COMPREHENSIVE EVALUATION")
        print("="*80)
        
        images = self.load_test_images(num_images)
        
        total_tests = len(images) * len(ATTACK_NAMES)
        current_test = 0
        
        for image, image_name in images:
            print(f"\n{'='*80}")
            print(f"Evaluating: {image_name}")
            print(f"{'='*80}")
            
            watermark = self.generate_watermark()
            
            for attack_id in range(len(ATTACK_NAMES)):
                current_test += 1
                print(f"\n[{current_test}/{total_tests}] Testing {ATTACK_NAMES[attack_id]}...")
                
                result = self.evaluate_single_image(image, watermark, attack_id, image_name)
                self.results.append(result)
                
                # Print metrics
                print(f"  PSNR: {result['psnr']:.2f} dB | SSIM: {result['ssim']:.4f} | BER: {result['ber']:.2f}% | Quality: {result['quality']}")
                
                # Save visualization
                safe_attack_name = result['attack_name'].replace(' ', '_').replace('(', '').replace(')', '')
                safe_image_name = os.path.splitext(image_name)[0]
                viz_path = os.path.join(self.output_dir, 'images', 
                                       f"{safe_image_name}_{safe_attack_name}.png")
                self.visualize_result(result, viz_path)
        
        print(f"\n{'='*80}")
        print("Evaluation Complete!")
        print(f"{'='*80}")
    
    def generate_summary_report(self):
        """Generate summary statistics and report"""
        print("\n" + "="*80)
        print("GENERATING SUMMARY REPORT")
        print("="*80)
        
        # Calculate average metrics per attack type
        attack_stats = {}
        for attack_id in range(len(ATTACK_NAMES)):
            attack_results = [r for r in self.results if r['attack_id'] == attack_id]
            if attack_results:
                attack_stats[ATTACK_NAMES[attack_id]] = {
                    'avg_psnr': np.mean([r['psnr'] for r in attack_results]),
                    'avg_ssim': np.mean([r['ssim'] for r in attack_results]),
                    'avg_ber': np.mean([r['ber'] for r in attack_results]),
                    'count': len(attack_results)
                }
        
        # Create summary visualization
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle('Performance Summary Across All Attacks', fontsize=16, fontweight='bold')
        
        attack_names = list(attack_stats.keys())
        psnr_values = [attack_stats[name]['avg_psnr'] for name in attack_names]
        ssim_values = [attack_stats[name]['avg_ssim'] for name in attack_names]
        ber_values = [attack_stats[name]['avg_ber'] for name in attack_names]
        
        # PSNR bar chart
        axes[0].bar(range(len(attack_names)), psnr_values, color='skyblue')
        axes[0].set_xlabel('Attack Type', fontweight='bold')
        axes[0].set_ylabel('PSNR (dB)', fontweight='bold')
        axes[0].set_title('Average PSNR', fontweight='bold')
        axes[0].set_xticks(range(len(attack_names)))
        axes[0].set_xticklabels([name.split('(')[0].strip() for name in attack_names], rotation=45, ha='right')
        axes[0].axhline(y=35, color='g', linestyle='--', label='Good (35 dB)')
        axes[0].axhline(y=30, color='orange', linestyle='--', label='Fair (30 dB)')
        axes[0].legend()
        axes[0].grid(axis='y', alpha=0.3)
        
        # SSIM bar chart
        axes[1].bar(range(len(attack_names)), ssim_values, color='lightgreen')
        axes[1].set_xlabel('Attack Type', fontweight='bold')
        axes[1].set_ylabel('SSIM', fontweight='bold')
        axes[1].set_title('Average SSIM', fontweight='bold')
        axes[1].set_xticks(range(len(attack_names)))
        axes[1].set_xticklabels([name.split('(')[0].strip() for name in attack_names], rotation=45, ha='right')
        axes[1].axhline(y=0.94, color='g', linestyle='--', label='Good (0.94)')
        axes[1].axhline(y=0.90, color='orange', linestyle='--', label='Fair (0.90)')
        axes[1].legend()
        axes[1].grid(axis='y', alpha=0.3)
        
        # BER bar chart
        axes[2].bar(range(len(attack_names)), ber_values, color='lightcoral')
        axes[2].set_xlabel('Attack Type', fontweight='bold')
        axes[2].set_ylabel('BER (%)', fontweight='bold')
        axes[2].set_title('Average BER', fontweight='bold')
        axes[2].set_xticks(range(len(attack_names)))
        axes[2].set_xticklabels([name.split('(')[0].strip() for name in attack_names], rotation=45, ha='right')
        axes[2].axhline(y=5, color='g', linestyle='--', label='Good (5%)')
        axes[2].axhline(y=10, color='orange', linestyle='--', label='Fair (10%)')
        axes[2].legend()
        axes[2].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        summary_path = os.path.join(self.output_dir, 'summary_metrics.png')
        plt.savefig(summary_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Summary visualization saved: {summary_path}")
        
        # Save detailed report as JSON
        report = {
            'evaluation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': len(self.results),
            'attack_statistics': attack_stats,
            'detailed_results': [
                {
                    'image_name': r['image_name'],
                    'attack_name': r['attack_name'],
                    'psnr': r['psnr'],
                    'ssim': r['ssim'],
                    'ber': r['ber'],
                    'quality': r['quality']
                }
                for r in self.results
            ]
        }
        
        report_path = os.path.join(self.output_dir, 'evaluation_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Detailed report saved: {report_path}")
        
        # Print summary to console
        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        for attack_name, stats in attack_stats.items():
            print(f"\n{attack_name}:")
            print(f"  PSNR: {stats['avg_psnr']:.2f} dB")
            print(f"  SSIM: {stats['avg_ssim']:.4f}")
            print(f"  BER:  {stats['avg_ber']:.2f}%")
            print(f"  Tests: {stats['count']}")
        
        print("\n" + "="*80)
        print(f"All results saved to: {self.output_dir}")
        print("="*80)


if __name__ == "__main__":
    print("="*80)
    print("WATERMARK EVALUATION SYSTEM")
    print("="*80)
    
    # Check if model exists
    model_path = os.path.join(MODEL_OUTPUT_PATH, 'final_model_weights.h5')
    if not os.path.exists(model_path):
        print(f"\nError: Model weights not found at {model_path}")
        print("Please train the model first using trainer.py or trainer_with_logging.py")
        exit(1)
    
    # Create evaluator
    evaluator = WatermarkEvaluator(model_path)
    
    # Run evaluation
    evaluator.evaluate_all_attacks(num_images=3)
    
    # Generate summary
    evaluator.generate_summary_report()
    
    print("\n✓ Evaluation complete!")
    print(f"✓ Check {evaluator.output_dir} for all results")
