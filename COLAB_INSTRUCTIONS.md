# 📘 Google Colab Instructions

Complete guide for using this watermarking system in Google Colab.

---

## 🎯 Why Use Colab?

✅ **Free GPU** - Train 3-5x faster  
✅ **No installation** - Works in browser  
✅ **No setup** - Everything pre-configured  
✅ **Easy sharing** - Share results instantly  

---

## 🚀 Getting Started

### Method 1: Direct Notebook Link (Easiest)

1. **Upload to GitHub**
   - Create a GitHub repository
   - Upload all files from `watermark-cnn/` folder
   - Make repository **PUBLIC**

2. **Open in Colab**
   - Go to: https://colab.research.google.com/
   - Click: **File** → **Open notebook** → **GitHub** tab
   - Enter: `https://github.com/Mehulsri07/watermark-cnn`
   - Select: `watermark_colab.ipynb`

3. **Enable GPU**
   - Click: **Runtime** → **Change runtime type**
   - Select: **GPU** (T4)
   - Click: **Save**

4. **Run**
   - Click: **Runtime** → **Run all**
   - Wait ~10 minutes
   - Done! ✓

### Method 2: Upload Notebook Directly

1. **Download Notebook**
   - Download `watermark_colab.ipynb` from this repository

2. **Upload to Colab**
   - Go to: https://colab.research.google.com/
   - Click: **File** → **Upload notebook**
   - Select: `watermark_colab.ipynb`

3. **Enable GPU** (same as above)

4. **Update GitHub URL**
   - In the second code cell, replace `Mehulsri07` with your GitHub username
   - Or upload files manually (see Method 3)

5. **Run** (same as above)

### Method 3: Manual File Upload

If you don't want to use GitHub:

1. **Open Colab**
   - Go to: https://colab.research.google.com/
   - Create new notebook

2. **Upload Files**
   ```python
   from google.colab import files
   import zipfile
   
   # Upload your watermark-cnn.zip
   uploaded = files.upload()
   
   # Extract
   !unzip watermark-cnn.zip
   %cd watermark-cnn
   ```

3. **Install Dependencies**
   ```python
   !pip install -q tensorflow-wavelets opencv-python scikit-image matplotlib
   ```

4. **Download Sample Images**
   ```python
   !python download_samples.py
   ```

5. **Train and Evaluate**
   ```python
   !python train_and_evaluate.py
   ```

---

## ⚙️ Configuration

### Adjust Training Parameters

Before running, you can modify settings:

```python
# Edit configs.py in Colab
!echo "EPOCHS = 20" >> configs.py
!echo "BATCH_SIZE = 4" >> configs.py
```

Or edit directly in the notebook:

```python
# In a code cell
import sys
sys.path.insert(0, '/content/watermark-cnn')

# Override configs
import configs
configs.EPOCHS = 20
configs.BATCH_SIZE = 4
```

### Download More Images

```python
# Download 50 training + 10 test images
!python download_samples.py 50 10
```

---

## 📊 Viewing Results

### Display Summary Chart

```python
from IPython.display import Image, display
display(Image('config_1_baseline/evaluation_results/summary_metrics.png'))
```

### View JSON Report

```python
import json
with open('config_1_baseline/evaluation_results/evaluation_report.json', 'r') as f:
    report = json.load(f)
    print(json.dumps(report, indent=2))
```

### Show All Visualizations

```python
import glob
from IPython.display import Image, display

images = glob.glob('config_1_baseline/evaluation_results/images/*.png')
for img in images:
    print(f"\n{img}:")
    display(Image(img, width=800))
```

---

## 💾 Downloading Results

### Download Everything

```python
# Create zip file
!zip -r results.zip config_1_baseline/

# Download
from google.colab import files
files.download('results.zip')
```

### Download Specific Files

```python
from google.colab import files

# Download model weights
files.download('config_1_baseline/final_model_weights.h5')

# Download report
files.download('config_1_baseline/evaluation_results/evaluation_report.json')

# Download summary chart
files.download('config_1_baseline/evaluation_results/summary_metrics.png')
```

---

## 🔧 Advanced Usage

### Mount Google Drive

Save results directly to your Google Drive:

```python
from google.colab import drive
drive.mount('/content/drive')

# Copy results to Drive
!cp -r config_1_baseline/ /content/drive/MyDrive/watermark_results/
```

### Use Your Own Images from Drive

```python
from google.colab import drive
drive.mount('/content/drive')

# Copy images from Drive
!cp /content/drive/MyDrive/my_images/*.jpg train_images/
!cp /content/drive/MyDrive/my_test_images/*.jpg test_images/
```

### Train with Custom Dataset

```python
# Upload your images
from google.colab import files
import os

os.makedirs('train_images', exist_ok=True)
os.makedirs('test_images', exist_ok=True)

print("Upload training images:")
uploaded = files.upload()
for filename in uploaded.keys():
    !mv {filename} train_images/

print("Upload test images:")
uploaded = files.upload()
for filename in uploaded.keys():
    !mv {filename} test_images/
```

---

## ⏱️ Expected Runtime

| Configuration | GPU Type | Time |
|--------------|----------|------|
| 10 epochs, 20 images | T4 (Free) | ~5 min |
| 20 epochs, 50 images | T4 (Free) | ~10 min |
| 50 epochs, 100 images | T4 (Free) | ~25 min |
| 10 epochs, 20 images | V100 (Pro) | ~2 min |

---

## 🐛 Troubleshooting

### "Runtime disconnected"
- Colab free tier has time limits
- Save results to Drive periodically
- Use shorter training runs

### "Out of memory"
- Reduce `BATCH_SIZE` to 1
- Use fewer training images
- Restart runtime and try again

### "Module not found"
- Run: `!pip install tensorflow-wavelets opencv-python scikit-image`
- Restart runtime

### "No images found"
- Run: `!python download_samples.py`
- Or upload images manually

### Slow download speeds
- Use Google Drive mount instead
- Download only essential files

---

## 💡 Tips for Best Results

1. **Use GPU** - Always enable GPU for faster training
2. **More epochs** - 20-50 epochs for better accuracy
3. **More images** - 50-200 training images recommended
4. **Save to Drive** - Mount Drive to save results automatically
5. **Monitor progress** - Watch the training output
6. **Test incrementally** - Start with 10 epochs, then increase

---

## 📱 Sharing Results

### Share Notebook

1. Click: **Share** button (top right)
2. Change access to: **Anyone with the link**
3. Copy and share the link

### Share Results

1. Download results.zip
2. Upload to Google Drive
3. Share Drive link

Or:

1. Mount Drive
2. Save results to Drive
3. Share Drive folder

---

## 🆘 Need Help?

- 📖 Check [README.md](README.md) for more details
- 📘 Read [QUICKSTART.md](QUICKSTART.md) for basics
- 🐛 Open an [issue](https://github.com/Mehulsri07/watermark-cnn/issues)
- ⭐ Star the repo if it helps!

---

**Happy watermarking in Colab! 🎨☁️**
