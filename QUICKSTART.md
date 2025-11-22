# 🚀 Quick Start Guide

Get started with watermarking in 3 simple steps!

---

## Option 1: Google Colab (Easiest - 10 minutes)

**No installation required! Works in your browser with free GPU.**

### Step 1: Open Colab
Click here: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Mehulsri07/watermark-cnn/blob/main/watermark_colab.ipynb)

### Step 2: Enable GPU
- Click: **Runtime** → **Change runtime type**
- Select: **GPU**
- Click: **Save**

### Step 3: Run
- Click: **Runtime** → **Run all**
- Wait ~10 minutes
- Done! ✓

**That's it!** Results will appear automatically.

---

## Option 2: Local Installation (15 minutes)

**For running on your own computer.**

### Step 1: Clone Repository
```bash
git clone https://github.com/Mehulsri07/watermark-cnn.git
cd watermark-cnn
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download Sample Images
```bash
python download_samples.py
```

This downloads 20 training + 5 test images automatically.

### Step 4: Train and Evaluate
```bash
python train_and_evaluate.py
```

Wait ~10-15 minutes (CPU) or ~3-5 minutes (GPU).

### Step 5: View Results
Results are saved to `config_1_baseline/evaluation_results/`:
- `summary_metrics.png` - Performance charts
- `evaluation_report.json` - Detailed metrics
- `images/` - Visual comparisons

---

## What You Get

After training, you'll have:

✅ **Trained model** - Ready to embed watermarks  
✅ **Performance metrics** - PSNR, SSIM, BER for all attacks  
✅ **Visual results** - Before/after comparisons  
✅ **Detailed report** - JSON with all statistics  

---

## Next Steps

### Improve Results
```python
# Edit configs.py
EPOCHS = 20              # More training
BATCH_SIZE = 4           # Larger batches (if you have GPU memory)
```

### Add More Images
```bash
# Download more samples
python download_samples.py 50 10  # 50 train, 10 test
```

### Use Your Own Images
1. Add images to `train_images/` folder
2. Add images to `test_images/` folder
3. Run: `python train_and_evaluate.py`

### Test Single Image
```python
from models.wavetf_model import WaveTFModel
import numpy as np
import cv2

# Load model
model = WaveTFModel(image_size=(256, 256, 1), watermark_size=(256,))
model = model.get_model()
model.load_weights('config_1_baseline/final_model_weights.h5')

# Load your image
img = cv2.imread('your_image.jpg', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (256, 256))
img = img.astype(np.float32) / 255.0
img = np.expand_dims(img, axis=-1)
img = np.expand_dims(img, axis=0)

# Generate watermark
watermark = np.random.randint(0, 2, size=(1, 256)).astype(np.float32)
attack_id = np.array([[0]], dtype=np.int32)  # 0 = no attack

# Embed watermark
watermarked, extracted = model.predict([img, watermark, attack_id])

# Save result
cv2.imwrite('watermarked.jpg', (watermarked[0].squeeze() * 255).astype(np.uint8))
print("✓ Watermark embedded!")
```

---

## Troubleshooting

### "No images found"
- Run: `python download_samples.py`
- Or manually add images to `train_images/` and `test_images/`

### "Out of memory"
- Reduce `BATCH_SIZE` in `configs.py`
- Use fewer training images
- Use Colab with GPU

### "Module not found"
- Run: `pip install -r requirements.txt`

### Slow training
- Use GPU (Colab or local)
- Reduce `EPOCHS` for testing
- Reduce number of training images

---

## Need Help?

- 📖 Read the full [README.md](README.md)
- 🐛 Open an [issue](https://github.com/Mehulsri07/watermark-cnn/issues)
- ⭐ Star the repo if it helps!

---

**Happy watermarking! 🎨**
