# CNN-Based Image Watermarking

Deep learning watermarking system using CNNs and Discrete Wavelet Transform.

## Quick Start

### Kaggle (Recommended)
1. Upload `watermark_kaggle.ipynb` to Kaggle
2. Enable GPU (Settings → GPU T4 x2)
3. Run all cells

### Google Colab
1. Upload `watermark_colab.ipynb` to Colab
2. Enable GPU (Runtime → GPU)
3. Run all cells

### Local
```bash
pip install -r requirements.txt
python download_samples.py
python train_and_evaluate.py
```

## Files

**Notebooks:**
- `watermark_kaggle.ipynb` - Kaggle notebook
- `watermark_colab.ipynb` - Colab notebook

**Core Scripts:**
- `train_and_evaluate.py` - Train and evaluate
- `trainer.py` - Training only
- `evaluate_model.py` - Evaluation only
- `embed_and_extract.py` - Embed/extract watermarks
- `download_samples.py` - Download sample images
- `configs.py` - Configuration

**Modules:**
- `models/` - Model architectures
- `attacks/` - Attack implementations
- `data_loaders/` - Data loading
- `utils/` - Utilities

## Configuration

Edit `configs.py`:
```python
EPOCHS = 10
BATCH_SIZE = 2
```

## Requirements

- Python 3.8+
- TensorFlow 2.8+
- See `requirements.txt`

## License

MIT License
