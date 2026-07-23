# DWT+CNN Image Watermarking 🖼️🔐

A deep learning-based digital image watermarking system that utilizes Discrete Wavelet Transform (DWT) and Convolutional Neural Networks (CNNs). This repository contains the architecture, training scripts, and implementation codebase accompanying our co-authored IEEE research paper.

## 🚀 Overview

Digital asset protection requires watermarks that are invisible to the human eye but robust enough to survive image manipulation and compression. This project leverages the mathematical precision of frequency-domain embedding (DWT) alongside the feature-extraction power of deep generative AI (CNNs) to create a highly secure, non-destructive watermarking protocol.

## ✨ Key Features

* **Frequency-Domain Embedding:** Utilizes Discrete Wavelet Transform to embed data securely within the high and low-frequency bands of an image.
* **Deep Learning Extraction:** A custom-trained Convolutional Neural Network designed to recover hidden watermarks even after image distortion.
* **High Imperceptibility:** Ensures visual fidelity of the original host image remains completely intact.
* **Robustness:** Resilient against common image processing attacks such as cropping, noise addition, and JPEG compression.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Deep Learning Framework:** TensorFlow / Keras (or PyTorch)
* **Image Processing:** OpenCV, SciPy, NumPy
* **Research Standard:** Architected for journal-grade evaluation and benchmarking.

## 📦 Getting Started

1. **Clone the repository:**
   ```bash
