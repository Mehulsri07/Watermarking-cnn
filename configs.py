"""
Configuration file for watermarking system
Modify these settings to customize training and evaluation
"""
import os

# ============================================================================
# IMAGE AND WATERMARK SETTINGS
# ============================================================================
IMAGE_SIZE = (256, 256, 1)      # Image dimensions (height, width, channels)
WATERMARK_SIZE = (16 * 16,)     # Watermark size (256 bits = 16x16)

# ============================================================================
# TRAINING PARAMETERS
# ============================================================================
EPOCHS = 10                      # Number of training epochs (increase for better results)
BATCH_SIZE = 2                   # Batch size (increase if you have more GPU memory)
LEARNING_RATE = 0.001            # Learning rate for Adam optimizer

# ============================================================================
# LOSS WEIGHTS
# ============================================================================
IMAGE_LOSS_WEIGHT = 33.0         # Weight for image reconstruction loss
WATERMARK_LOSS_WEIGHT = 0.2      # Weight for watermark extraction loss

# ============================================================================
# ATTACK CONFIGURATION
# ============================================================================
# Attack IDs:
# 0: No attack (baseline)
# 1: Combined attack (2-3 random attacks) - RECOMMENDED for training
# 2: Gaussian noise
# 3: JPEG compression
# 4: Cropping
# 5: Scaling
# 6: Salt & Pepper noise
ATTACK_MAX_ID = 6  # Maximum attack ID (0 to 6 = 7 attack types)

# ============================================================================
# PATHS
# ============================================================================
MODEL_OUTPUT_PATH = 'config_1_baseline/'
TRAIN_IMAGES_PATH = 'train_images/'
TEST_IMAGES_PATH = 'test_images/'

# Create directories if they don't exist
os.makedirs(MODEL_OUTPUT_PATH, exist_ok=True)
os.makedirs(TRAIN_IMAGES_PATH, exist_ok=True)
os.makedirs(TEST_IMAGES_PATH, exist_ok=True)

# ============================================================================
# TIPS FOR BETTER RESULTS
# ============================================================================
# 1. Increase EPOCHS to 20-50 for better accuracy
# 2. Add more training images (50-200 recommended)
# 3. Use GPU for faster training
# 4. Adjust loss weights if needed
# 5. Use combined attack (ID=1) during training for robustness
