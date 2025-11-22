# 🔧 Colab Troubleshooting Guide

Common errors and how to fix them.

---

## ❌ Error: "FileNotFoundError: No such file or directory"

### Symptom
```
FileNotFoundError: No such file or directory: 'config_1_baseline/evaluation_results/summary_metrics.png'
```

### Cause
Training hasn't completed yet, so results don't exist.

### Fix
1. ✅ Make sure you ran the training cell (Step 4)
2. ✅ Wait for training to complete (~5-10 minutes)
3. ✅ Look for "✓ COMPLETE!" message
4. ✅ Then run the results cells

**Don't skip cells!** Run them in order.

---

## ❌ Error: "ModuleNotFoundError: No module named 'models'"

### Symptom
```
ModuleNotFoundError: No module named 'models'
```

### Cause
Not in the correct directory or imports broken.

### Fix
```python
# Check current directory
import os
print(os.getcwd())

# Should be: /content/Watermarking-cnn
# If not, run:
%cd Watermarking-cnn
```

---

## ❌ Error: "Repository not found" (404)

### Symptom
```
fatal: repository 'https://github.com/Mehulsri07/Watermarking-cnn.git' not found
```

### Cause
Repository doesn't exist or is PRIVATE.

### Fix
1. ✅ Check repository exists: https://github.com/Mehulsri07/Watermarking-cnn
2. ✅ Make sure it's PUBLIC:
   - Go to Settings → Danger Zone → Change visibility → Public
3. ✅ Wait 2-3 minutes after making it public
4. ✅ Restart Colab runtime: Runtime → Restart runtime

---

## ❌ Error: "No images found"

### Symptom
```
No training images found!
```

### Cause
Image download failed or was skipped.

### Fix
Run the download cell again:
```python
# Re-run Step 2: Download Sample Images
download_samples(num_train=20, num_test=5)
```

Or check if images exist:
```python
import os
print("Training images:", len(os.listdir('train_images')))
print("Test images:", len(os.listdir('test_images')))
```

---

## ❌ Error: "Out of memory"

### Symptom
```
ResourceExhaustedError: OOM when allocating tensor
```

### Cause
Not enough GPU memory.

### Fix
1. **Reduce batch size:**
   ```python
   # In Step 3, change:
   BATCH_SIZE = 1  # Instead of 2
   ```

2. **Restart runtime:**
   - Runtime → Restart runtime
   - Run cells again

3. **Use fewer images:**
   ```python
   download_samples(num_train=10, num_test=3)
   ```

---

## ❌ Error: "Runtime disconnected"

### Symptom
Colab disconnects during training.

### Cause
- Idle timeout (free tier)
- Browser tab inactive
- Network issues

### Fix
1. **Keep tab active** - Don't switch tabs during training
2. **Use Colab Pro** - Longer runtime limits
3. **Run in shorter sessions:**
   ```python
   EPOCHS = 5  # Instead of 10
   ```

---

## ❌ Error: "Permission denied"

### Symptom
```
PermissionError: [Errno 13] Permission denied
```

### Cause
Trying to write to protected directory.

### Fix
Make sure you're in the project directory:
```python
%cd /content/Watermarking-cnn
```

---

## ❌ Error: "CUDA out of memory"

### Symptom
```
CUDA out of memory
```

### Cause
GPU memory full.

### Fix
1. **Restart runtime:**
   - Runtime → Restart runtime

2. **Reduce batch size:**
   ```python
   BATCH_SIZE = 1
   ```

3. **Clear GPU memory:**
   ```python
   import tensorflow as tf
   tf.keras.backend.clear_session()
   ```

---

## ❌ Error: "No GPU available"

### Symptom
```
GPU Available: ✗ NO
```

### Cause
GPU not enabled or quota exceeded.

### Fix
1. **Enable GPU:**
   - Runtime → Change runtime type → GPU → Save

2. **Check quota:**
   - Free tier has limited GPU hours
   - Wait or upgrade to Colab Pro

3. **Verify:**
   ```python
   import tensorflow as tf
   print(tf.config.list_physical_devices('GPU'))
   ```

---

## ❌ Training is Very Slow

### Symptom
Training takes >30 minutes.

### Cause
Using CPU instead of GPU.

### Fix
1. **Check GPU is enabled:**
   ```python
   import tensorflow as tf
   print("GPU:", tf.config.list_physical_devices('GPU'))
   ```

2. **Enable GPU:**
   - Runtime → Change runtime type → GPU → Save
   - Restart runtime

3. **Expected times:**
   - GPU: 5-10 minutes
   - CPU: 30-60 minutes

---

## ❌ Error: "Invalid argument"

### Symptom
```
InvalidArgumentError: indices[0] = X is not in [0, Y)
```

### Cause
Data loading issue or corrupted images.

### Fix
1. **Re-download images:**
   ```python
   !rm -rf train_images test_images
   download_samples(num_train=20, num_test=5)
   ```

2. **Check image count:**
   ```python
   import os
   print("Train:", len(os.listdir('train_images')))
   print("Test:", len(os.listdir('test_images')))
   ```

---

## ✅ General Troubleshooting Steps

### 1. Restart Runtime
```
Runtime → Restart runtime
```
Then run all cells again from the top.

### 2. Check Directory
```python
import os
print("Current dir:", os.getcwd())
print("Files:", os.listdir('.'))
```

### 3. Verify GPU
```python
import tensorflow as tf
print("TensorFlow:", tf.__version__)
print("GPU:", tf.config.list_physical_devices('GPU'))
```

### 4. Check Files Exist
```python
import os
print("train_images:", os.path.exists('train_images'))
print("test_images:", os.path.exists('test_images'))
print("models/:", os.path.exists('models'))
```

### 5. Clear and Restart
```
Runtime → Factory reset runtime
```
This clears everything and starts fresh.

---

## 📊 Expected Output

### After Training (Step 4)
```
================================================================================
STEP 1: TRAINING MODEL
================================================================================
...
Epoch 10/10
...
✓ Model saved to: config_1_baseline/final_model_weights.h5

================================================================================
STEP 2: EVALUATING MODEL WITH ALL ATTACKS
================================================================================
...
✓ Evaluation complete!

================================================================================
STEP 3: GENERATING SUMMARY REPORT
================================================================================
...
✓ All results saved to: config_1_baseline/evaluation_results
================================================================================
✓ COMPLETE! Training and evaluation finished successfully
================================================================================
```

### After Results Check
```
✓ Model weights: Found
✓ Evaluation report: Found
✓ Summary chart: Found
✓ Result images: Found

============================================================
✅ Training completed successfully!
You can now view the results below.
============================================================
```

---

## 🆘 Still Having Issues?

1. **Read error message carefully** - It usually tells you what's wrong

2. **Check each step:**
   - [ ] GPU enabled
   - [ ] Repository cloned
   - [ ] Dependencies installed
   - [ ] Images downloaded
   - [ ] Training completed

3. **Try fresh start:**
   - Runtime → Factory reset runtime
   - Run all cells from top

4. **Check GitHub:**
   - Repository is PUBLIC
   - All files are there
   - Correct repository name

5. **Ask for help:**
   - Copy the full error message
   - Note which cell failed
   - Open an issue on GitHub

---

## 💡 Tips for Success

1. **Run cells in order** - Don't skip steps
2. **Wait for completion** - Don't interrupt training
3. **Keep tab active** - Prevents disconnection
4. **Use GPU** - Much faster than CPU
5. **Start small** - Test with fewer epochs first
6. **Save results** - Download before closing

---

**Most common fix:** Restart runtime and run all cells in order! 🔄
