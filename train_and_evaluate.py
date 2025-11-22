"""
Integrated training and evaluation script
Trains the model and automatically evaluates it with all attacks
"""
import sys
import os

# Add current directory to Python path to fix imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
# Also add current working directory
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

import tensorflow as tf
import numpy as np
from datetime import datetime
from configs import *
from models.wavetf_model import WaveTFModel
from data_loaders.merged_data_loader import MergedDataLoader

# Import evaluation components
import matplotlib.pyplot as plt
import json
import cv2
from utils.metrics import calculate_psnr, calculate_ssim, calculate_ber, evaluate_quality

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

class IntegratedTrainer:
    def __init__(self):
        self.model = None
        self.data_loader = None
        self.output_dir = MODEL_OUTPUT_PATH
        self.eval_dir = os.path.join(self.output_dir, 'evaluation_results')
        
    def train(self):
        """Train the model"""
        print("="*80)
        print("STEP 1: TRAINING MODEL")
        print("="*80)
        
        # Create model
        print("\nBuilding model...")
        wavetf_model = WaveTFModel(image_size=IMAGE_SIZE, watermark_size=WATERMARK_SIZE)
        self.model = wavetf_model.get_model()
        
        # Compile model
        print("Compiling model...")
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
            loss={
                'embedded_image': 'mse',
                'output_watermark': 'mae'
            },
            loss_weights={
                'embedded_image': IMAGE_LOSS_WEIGHT,
                'output_watermark': WATERMARK_LOSS_WEIGHT
            },
            metrics=['accuracy']
        )
        
        # Load data
        print("Loading training data...")
        train_dataset = MergedDataLoader(
            image_base_path=TRAIN_IMAGES_PATH,
            image_channels=[0],
            image_convert_type=tf.float32,
            watermark_size=WATERMARK_SIZE,
            attack_min_id=0,
            attack_max_id=ATTACK_MAX_ID,
            batch_size=BATCH_SIZE
        ).get_data_loader()
        
        print(f"\nTraining configuration:")
        print(f"  Epochs: {EPOCHS}")
        print(f"  Batch size: {BATCH_SIZE}")
        print(f"  Learning rate: {LEARNING_RATE}")
        print(f"  Image loss weight: {IMAGE_LOSS_WEIGHT}")
        print(f"  Watermark loss weight: {WATERMARK_LOSS_WEIGHT}")
        
        # Train
        print("\nStarting training...")
        print("-"*80)
        
        history = self.model.fit(
            train_dataset,
            epochs=EPOCHS,
            verbose=1
        )
        
        # Save model
        print("\nSaving model...")
        model_path = os.path.join(self.output_dir, 'final_model_weights.h5')
        self.model.save_weights(model_path)
        print(f"✓ Model saved to: {model_path}")
        
        return history
    
    def evaluate(self):
        """Evaluate the model with all attacks"""
        print("\n" + "="*80)
        print("STEP 2: EVALUATING MODEL WITH ALL ATTACKS")
        print("="*80)
        
        # Create output directories
        os.makedirs(self.eval_dir, exist_ok=True)
        os.makedirs(os.path.join(self.eval_dir, 'images'), exist_ok=True)
        
        # Load test images
        print(f"\nLoading test images from {TEST_IMAGES_PATH}...")
        test_images = self._load_test_images(num_images=3)
        print(f"✓ Loaded {len(test_images)} test images")
        
        # Run evaluation
        results = []
        total_tests = len(test_images) * len(ATTACK_NAMES)
        current_test = 0
        
        print("\nRunning evaluation tests...")
        print("-"*80)
        
        for image, image_name in test_images:
            print(f"\nEvaluating: {image_name}")
            watermark = self._generate_watermark()
            
            for attack_id in range(len(ATTACK_NAMES)):
                current_test += 1
                attack_name = ATTACK_NAMES[attack_id]
                
                print(f"  [{current_test}/{total_tests}] {attack_name}...", end=" ")
                
                result = self._evaluate_single(image, watermark, attack_id, image_name)
                results.append(result)
                
                print(f"PSNR: {result['psnr']:.2f} dB | SSIM: {result['ssim']:.4f} | BER: {result['ber']:.2f}%")
                
                # Save visualization
                self._save_visualization(result)
        
        print("\n" + "-"*80)
        print("✓ Evaluation complete!")
        
        # Generate summary
        self._generate_summary(results)
        
        return results
    
    def _load_test_images(self, num_images=3):
        """Load test images"""
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
        
        return images
    
    def _generate_watermark(self):
        """Generate random watermark"""
        return np.random.randint(0, 2, size=WATERMARK_SIZE).astype(np.float32)
    
    def _evaluate_single(self, image, watermark, attack_id, image_name):
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
        
        return {
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
    
    def _save_visualization(self, result):
        """Save visualization for a result"""
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
        
        # Difference
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
        
        # Metrics
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
        
        safe_attack_name = result['attack_name'].replace(' ', '_').replace('(', '').replace(')', '')
        safe_image_name = os.path.splitext(result['image_name'])[0]
        save_path = os.path.join(self.eval_dir, 'images', f"{safe_image_name}_{safe_attack_name}.png")
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _generate_summary(self, results):
        """Generate summary report"""
        print("\n" + "="*80)
        print("STEP 3: GENERATING SUMMARY REPORT")
        print("="*80)
        
        # Calculate statistics
        attack_stats = {}
        for attack_id in range(len(ATTACK_NAMES)):
            attack_results = [r for r in results if r['attack_id'] == attack_id]
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
        
        # PSNR
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
        
        # SSIM
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
        
        # BER
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
        summary_path = os.path.join(self.eval_dir, 'summary_metrics.png')
        plt.savefig(summary_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"\n✓ Summary visualization: {summary_path}")
        
        # Save JSON report
        report = {
            'evaluation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': len(results),
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
                for r in results
            ]
        }
        
        report_path = os.path.join(self.eval_dir, 'evaluation_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✓ Detailed report: {report_path}")
        
        # Print summary
        print("\n" + "-"*80)
        print("SUMMARY STATISTICS")
        print("-"*80)
        for attack_name, stats in attack_stats.items():
            print(f"\n{attack_name}:")
            print(f"  PSNR: {stats['avg_psnr']:.2f} dB")
            print(f"  SSIM: {stats['avg_ssim']:.4f}")
            print(f"  BER:  {stats['avg_ber']:.2f}%")
            print(f"  Tests: {stats['count']}")
        
        print("\n" + "="*80)
        print(f"✓ All results saved to: {self.eval_dir}")
        print("="*80)


if __name__ == "__main__":
    print("="*80)
    print("INTEGRATED TRAINING AND EVALUATION SYSTEM")
    print("="*80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    trainer = IntegratedTrainer()
    
    # Step 1: Train
    history = trainer.train()
    
    # Step 2: Evaluate
    results = trainer.evaluate()
    
    print("\n" + "="*80)
    print("✓ COMPLETE! Training and evaluation finished successfully")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
