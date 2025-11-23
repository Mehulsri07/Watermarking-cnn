"""
Script to generate complete source code documentation
Combines all Python files into one comprehensive text file
"""
import os

# Define all files to include
files_to_include = [
    ("Configuration", [
        ("configs.py", "Main configuration for training and evaluation"),
        ("requirements.txt", "Python package dependencies"),
    ]),
    ("Main Scripts", [
        ("train_and_evaluate.py", "Integrated training and evaluation script"),
        ("trainer.py", "Training only script"),
        ("evaluate_model.py", "Evaluation only script"),
        ("embed_and_extract.py", "Demo script for embedding/extracting watermarks"),
        ("wavetf.py", "Wavelet transform wrapper"),
    ]),
    ("Model Architecture", [
        ("models/base_model.py", "Abstract base model class"),
        ("models/wavetf_model.py", "Main WaveTF watermarking model"),
    ]),
    ("Attack Implementations", [
        ("attacks/base_attack.py", "Abstract base attack class"),
        ("attacks/stupid_attack.py", "No attack (baseline)"),
        ("attacks/combined_attack.py", "Combined attack (2-3 random attacks)"),
        ("attacks/gaussian_noise_attack.py", "Gaussian noise attack"),
        ("attacks/jpeg_attack.py", "JPEG compression attack"),
        ("attacks/cropping_attack.py", "Cropping attack"),
        ("attacks/scaling_attack.py", "Scaling attack"),
        ("attacks/salt_pepper_attack.py", "Salt & pepper noise attack"),
        ("attacks/drop_out_attack.py", "Dropout attack"),
        ("attacks/rotation_attack.py", "Rotation attack"),
    ]),
    ("Data Loaders", [
        ("data_loaders/base_data_loader.py", "Abstract base data loader"),
        ("data_loaders/configs.py", "Data loader configuration"),
        ("data_loaders/merged_data_loader.py", "Combined data loader"),
        ("data_loaders/image_data_loaders/image_data_loader.py", "Image loading"),
        ("data_loaders/watermark_data_loaders/watermark_data_loader.py", "Watermark generation"),
        ("data_loaders/attack_id_data_loader/attack_id_data_loader.py", "Attack ID generation"),
    ]),
    ("Utilities", [
        ("utils/metrics.py", "Evaluation metrics (PSNR, SSIM, BER)"),
    ]),
]

output_file = "ALL_SOURCE_CODE.txt"

with open(output_file, 'w', encoding='utf-8') as out:
    # Write header
    out.write("=" * 80 + "\n")
    out.write("COMPLETE SOURCE CODE - WATERMARKING CNN PROJECT\n")
    out.write("=" * 80 + "\n")
    out.write("Generated: 2025-11-23\n")
    out.write("Python Version: 3.13.5\n")
    out.write("Pip Version: 25.3\n")
    out.write("System: Windows\n\n")
    out.write("This file contains ALL Python source code from the project.\n")
    out.write("Each file is clearly labeled with its path and purpose.\n")
    out.write("=" * 80 + "\n\n")
    
    # Process each section
    for section_name, files in files_to_include:
        out.write("\n" + "=" * 80 + "\n")
        out.write(f"SECTION: {section_name.upper()}\n")
        out.write("=" * 80 + "\n\n")
        
        for file_path, description in files:
            out.write("#" * 80 + "\n")
            out.write(f"# FILE: {file_path}\n")
            out.write(f"# PURPOSE: {description}\n")
            out.write("#" * 80 + "\n\n")
            
            # Read and write file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    out.write(content)
                    out.write("\n\n")
            except FileNotFoundError:
                out.write(f"# ERROR: File not found: {file_path}\n\n")
            except Exception as e:
                out.write(f"# ERROR reading file: {e}\n\n")
    
    # Write footer
    out.write("\n" + "=" * 80 + "\n")
    out.write("END OF SOURCE CODE DOCUMENTATION\n")
    out.write("=" * 80 + "\n")

print(f"✓ Complete source code documentation generated: {output_file}")
print(f"✓ File size: {os.path.getsize(output_file):,} bytes")
