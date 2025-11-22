# 🚀 Kaggle Setup Guide

Complete guide for running the watermarking system on Kaggle.

---

## 🎯 Why Kaggle?

✅ **Free GPU** - 30 hours/week GPU quota  
✅ **Better than Colab** - More stable, longer sessions  
✅ **Easy sharing** - Public notebooks  
✅ **Persistent storage** - Save outputs automatically  

---

## 📝 Quick Start (3 Steps)

### Step 1: Create New Notebook

1. Go to: https://www.kaggle.com/
2. Click: **"New Notebook"**
3. Or upload: `watermark_kaggle.ipynb`

### Step 2: Enable GPU & Internet

**Settings (right sidebar):**
- **Accelerator:** GPU T4 x2 (or P100)
- **Internet:** ON
- **Persistence:** Files only

Click **"Save"**

### Step 3: Run All Cells

- Click: **"Run All"** (or Shift+Enter on each cell)
- Wait: ~20-25 minutes
- Done! ✓

---

## 🔧 Kaggle-Specific Setup

### Differences from Colab

| Feature | Colab | Kaggle |
|---------|-------|--------|
| Working Dir | `/content/` | `/kaggle/working/` |
| GPU | T4 (free) | T4 x2 or P100 |
| Session | 12 hours | 9-12 hours |
| Internet | Always on | Must enable |
| Outputs | Manual download | Auto-saved |
| File Upload | `files.upload()` | Add dataset |

### Kaggle Advantages

✅ **Better GPU** - T4 x2 or P100 available  
✅ **Auto-save outputs** - Files in `/kaggle/working/` saved automatically  
✅ **Longer sessions** - More stable than Colab  
✅ **Public sharing** - Easy to share notebooks  
✅ **Version control** - Built-in versioning  

---

## 📁 Directory Structure

```
/kaggle/
├── input/          # Read-only datasets
├── working/        # Your working directory (saved as output)
│   └── Watermarking-cnn/
│       ├── models/
│       ├── attacks/
│       ├── data_loaders/
│       ├── utils/
│       ├── train_images/
│       ├── test_images/
│       └── config_1_baseline/
└── temp/           # Temporary files (not saved)
```

**Important:** Only files in `/kaggle/working/` are saved as outputs!

---

## 🚀 Step-by-Step Guide

### 1. Setup (5 minutes)

```python
# Check GPU
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))

# Clone repo
!git clone https://github.com/Mehulsri07/Watermarking-cnn.git
%cd Watermarking-cnn

# Install dependencies
!pip install -q 'numpy<2.0' tensorflow-wavelets opencv-python scikit-image
```

### 2. Download Images (2 minutes)

```python
# Downloads 80 training + 20 test images
!python download_samples.py
```

Or use the function in the notebook.

### 3. Train (15-20 minutes)

```python
# Trains for 50 epochs with batch size 10
!python train_and_evaluate.py
```

### 4. View Results (instant)

Results display automatically in the notebook!

### 5. Save Outputs (optional)

```python
# Copy to /kaggle/working/ for auto-save
import shutil
shutil.copy('config_1_baseline/final_model_weights.h5', '/kaggle/working/')
```

---

## 📊 Expected Performance

### Training Time

| GPU Type | Time (50 epochs) |
|----------|------------------|
| T4 x2 | 15-20 minutes |
| P100 | 10-15 minutes |
| CPU | 2-3 hours ❌ |

### Results

| Metric | Expected |
|--------|----------|
| PSNR | 38-42 dB |
| SSIM | 0.95-0.98 |
| BER | 1-3% |

---

## 💾 Saving Results

### Automatic (Recommended)

Files in `/kaggle/working/` are automatically saved as outputs:

```python
import shutil
import os

# Copy important files
shutil.copy('config_1_baseline/final_model_weights.h5', '/kaggle/working/')
shutil.copy('config_1_baseline/evaluation_results/evaluation_report.json', '/kaggle/working/')
shutil.copy('config_1_baseline/evaluation_results/summary_metrics.png', '/kaggle/working/')
```

### Download

1. Click **"Output"** tab (top right)
2. See your saved files
3. Click download icon

---

## 🐛 Troubleshooting

### "Internet is off"

**Fix:** Settings → Internet → ON → Save

### "No GPU available"

**Fix:** Settings → Accelerator → GPU T4 x2 → Save

### "ModuleNotFoundError"

**Fix:** Make sure you're in the right directory:
```python
import os
os.chdir('/kaggle/working/Watermarking-cnn')
```

### "NumPy version error"

**Fix:** Install NumPy 1.x:
```python
!pip install -q 'numpy<2.0'
```

### "Out of memory"

**Fix:** Reduce batch size in configs.py:
```python
BATCH_SIZE = 5  # Instead of 10
```

### "Session expired"

Kaggle sessions last 9-12 hours. If expired:
1. Save your work
2. Restart session
3. Run cells again

---

## 🎯 Optimization Tips

### 1. Use Better GPU

Settings → Accelerator → **GPU P100** (if available)
- Faster than T4
- More memory

### 2. Increase Batch Size

If you have P100:
```python
BATCH_SIZE = 16  # Instead of 10
```

### 3. More Training Data

```python
download_samples(num_train=100, num_test=30)
```

### 4. More Epochs

```python
EPOCHS = 100  # Instead of 50
```

### 5. Save Checkpoints

Edit `trainer.py` to save every 10 epochs.

---

## 📤 Sharing Your Notebook

### Make Public

1. Click **"Share"** (top right)
2. Select: **"Public"**
3. Copy link
4. Share!

### Add to Profile

1. Go to your profile
2. Notebooks tab
3. Pin this notebook

### Get Upvotes

- Add good documentation
- Show clear results
- Explain your approach
- Help others in comments

---

## 🔄 Kaggle vs Colab

### Use Kaggle if:

✅ You want better GPU (P100)  
✅ You need longer sessions  
✅ You want auto-saved outputs  
✅ You're building a portfolio  

### Use Colab if:

✅ You need Google Drive integration  
✅ You prefer Google ecosystem  
✅ You want unlimited sessions (with Pro)  

**Recommendation:** Use Kaggle for this project!

---

## 📚 Additional Resources

### Kaggle Docs
- https://www.kaggle.com/docs/notebooks
- https://www.kaggle.com/docs/efficient-gpu-usage

### GPU Quota
- Free: 30 hours/week
- Check: Settings → Account → GPU Quota

### Datasets
- Can add datasets as input
- Useful for larger image collections

---

## ✅ Success Checklist

Before running:

- [ ] GPU enabled (T4 x2 or P100)
- [ ] Internet enabled
- [ ] Notebook saved
- [ ] All cells ready

After running:

- [ ] Training completed (50 epochs)
- [ ] Results displayed
- [ ] Outputs saved to `/kaggle/working/`
- [ ] Downloaded results

---

## 🎉 You're Ready!

Your Kaggle notebook is optimized and ready to run!

**Notebook:** `watermark_kaggle.ipynb`

**Expected time:** ~20-25 minutes total

**Expected results:** Excellent (PSNR: 38-42 dB)

**Good luck!** 🚀
