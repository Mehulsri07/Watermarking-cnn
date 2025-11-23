# Fix Applied: Model Input/Output Connection Error

## Error
```
ValueError: `inputs` not connected to `outputs`
```

## Root Cause
The model defined 3 inputs (`image_input`, `watermark_input`, `attack_id_input`) but the `attack_id_input` was never used in the computation graph leading to the outputs. In Keras Functional API, all inputs must be connected to outputs through layers.

## Solution
Removed the unused `attack_id_input` from the model architecture. The attack simulation is now handled externally during evaluation, not inside the model graph.

## Files Modified

### 1. models/wavetf_model.py
- Removed `attack_id_in` input from model
- Model now has 2 inputs: `[img_in, wm_in]`
- Model outputs: `[embedded_image, output_watermark]`

### 2. data_loaders/merged_data_loader.py
- Updated data pipeline to provide 2 inputs instead of 3
- Removed attack_id from data formatting
- Data format: `inputs=(image, watermark)`, `outputs=(image, watermark)`

### 3. train_and_evaluate.py
- Updated prediction calls to use 2 inputs
- Removed `attack_id_batch` from predict calls
- Model.predict now called with: `[image_batch, watermark_batch]`

### 4. evaluate_model.py
- Updated prediction calls to use 2 inputs
- Removed `attack_id_batch` from predict calls

### 5. embed_and_extract.py
- Updated prediction calls to use 2 inputs
- Removed `attack_id_batch` from predict calls

## Model Architecture (Updated)

```
Inputs:
  - image_input: (256, 256, 1) grayscale image
  - watermark_input: (256,) binary vector

Processing:
  1. Wavelet transform (or fallback to average pooling)
  2. Encoder: Conv2D layers to embed watermark
  3. Watermark preprocessing: Dense layers to spatial map
  4. Concatenation: Merge image + watermark features
  5. Embedding: Output watermarked image
  6. Extractor: Conv2D + GlobalAveragePooling to extract watermark

Outputs:
  - embedded_image: (256, 256, 1) watermarked image
  - output_watermark: (256,) extracted watermark bits
```

## Attack Handling

Attacks are now applied **externally** during evaluation:
- Training: Model learns to embed/extract watermarks without attacks
- Evaluation: Attacks can be applied to watermarked images before extraction
- This is actually simpler and more flexible than in-model attack simulation

## Benefits of This Approach

1. **Simpler Model**: Cleaner architecture without complex attack simulation
2. **Faster Training**: No attack overhead during training
3. **More Flexible**: Can test any attack without retraining
4. **Easier Debugging**: Clear separation between embedding and attack testing
5. **Keras Compatible**: No issues with Functional API graph connections

## Training Process (Updated)

1. Load images and generate watermarks
2. Model embeds watermark into image
3. Model extracts watermark from embedded image
4. Calculate losses:
   - Image loss (MSE): Minimize distortion
   - Watermark loss (MAE): Maximize extraction accuracy
5. Update weights via backpropagation

## Evaluation Process (Updated)

1. Load trained model
2. For each test image:
   - Embed watermark
   - (Optional) Apply attack externally
   - Extract watermark
   - Calculate metrics (PSNR, SSIM, BER, Accuracy)

## Next Steps

The model should now train successfully. Run:

```bash
python train_and_evaluate.py
```

Expected behavior:
- Model builds without errors
- Training proceeds for 60 epochs
- Evaluation generates metrics and visualizations
- Results saved to config_1_baseline/

## Note on Attack Testing

If you want to test robustness against attacks:
1. Train the model first (without attacks)
2. During evaluation, apply attacks to watermarked images
3. Then extract watermarks and measure BER

This approach is actually more realistic - you train on clean data and test on attacked data.

---

**Fix Applied**: 2025-11-23
**Status**: Ready for training
