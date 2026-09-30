# DWT+CNN Image Watermarking 🖼️🔐

A deep learning-based digital image watermarking system that utilizes Discrete Wavelet Transform (DWT) and Convolutional Neural Networks (CNNs). This repository contains the architecture, training scripts, and implementation codebase accompanying our co-authored IEEE research paper.

## 🚀 Overview

Digital asset protection requires watermarks that are invisible to the human eye but robust enough to survive image manipulation and compression. This project leverages the mathematical precision of frequency-domain embedding (DWT) alongside the feature-extraction power of a convolutional neural network, so the watermark stays invisible while still being recoverable after the image is attacked.

## ✨ Key Features

* **Frequency-Domain Embedding:** Utilizes Discrete Wavelet Transform to embed data securely within the high and low-frequency bands of an image.
* **Deep Learning Extraction:** A custom-trained Convolutional Neural Network designed to recover hidden watermarks even after image distortion.
* **High Imperceptibility:** Ensures visual fidelity of the original host image remains completely intact.
* **Robustness:** Resilient against common image processing attacks such as cropping, noise addition, and JPEG compression.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Deep Learning Framework:** TensorFlow / Keras (Keras 3 compatible), with a wavelet layer from `tensorflow-wavelets`
* **Image Processing:** OpenCV, scikit-image, SciPy, NumPy
* **Evaluation:** PSNR and SSIM for imperceptibility, bit error rate (BER) for watermark recovery

## ⚔️ Attacks tested

The model is trained and evaluated against attacks applied between embedding and extraction (see `attacks/`): Gaussian noise, salt-and-pepper noise, JPEG compression, cropping, scaling, rotation, dropout, and random combinations of 2-3 of these.

## 📦 Getting Started

1. **Clone the repository and install dependencies:**
   ```bash
   git clone https://github.com/Mehulsri07/Watermarking-cnn.git
   cd Watermarking-cnn
   pip install -r requirements.txt
   ```

2. **Add images.** Put training images in `../train_images/` and a few test images in `test_images/` (paths are set in `configs.py`). The paper runs used the full COCO training set; for a quick try, `python download_samples.py` fetches a small random sample.

3. **Train and evaluate** (256x256 grayscale images, 256-bit watermark, settings in `configs.py`):
   ```bash
   python train_and_evaluate.py
   ```
   Weights and evaluation results are written to `config_1_baseline/`.

4. **Embed and extract a watermark** on a test image under every attack, printing PSNR, SSIM and BER:
   ```bash
   python embed_and_extract.py
   ```

No local GPU? `watermark_colab.ipynb` and `watermark_kaggle.ipynb` run the same pipeline on Google Colab or Kaggle.

## 📄 Paper

This code accompanies an IEEE-format paper on DWT + CNN watermarking, co-authored with Manvik Talwar and Srajal Singh (Manipal University Jaipur).
