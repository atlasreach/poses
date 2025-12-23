#!/usr/bin/env python3
"""
Download ComfyUI models for Qwen Image Edit workflows
This script downloads all required models to the proper directories
"""

import os
from huggingface_hub import hf_hub_download, snapshot_download
from pathlib import Path

# Hugging Face token - load from environment variable
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Base ComfyUI models directory
BASE_DIR = Path("/workspace/ComfyUI/models")

def download_models():
    """Download all required models for Qwen Image Edit workflows"""

    print("🚀 Starting model downloads...")
    print(f"Base directory: {BASE_DIR}")

    # 1. Download UNET Model (bf16 version - 40GB)
    print("\n📦 Downloading UNET Model (qwen_image_edit_2509_bf16_3.safetensors)...")
    unet_dir = BASE_DIR / "unet"
    unet_dir.mkdir(parents=True, exist_ok=True)
    try:
        hf_hub_download(
            repo_id="Comfy-Org/Qwen-Image-Edit_ComfyUI",
            filename="split_files/diffusion_models/qwen_image_edit_2509_bf16_3.safetensors",
            local_dir=str(BASE_DIR / "unet"),
            local_dir_use_symlinks=False,
            token=HF_TOKEN
        )
        print("✅ UNET Model downloaded!")
    except Exception as e:
        print(f"❌ Error downloading UNET: {e}")

    # 2. Download Text Encoder (fp8 version)
    print("\n📦 Downloading Text Encoder (qwen_2.5_vl_7b_fp8_scaled.safetensors)...")
    text_encoder_dir = BASE_DIR / "text_encoders"
    text_encoder_dir.mkdir(parents=True, exist_ok=True)
    try:
        hf_hub_download(
            repo_id="Comfy-Org/Qwen-Image_ComfyUI",
            filename="split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors",
            local_dir=str(text_encoder_dir),
            local_dir_use_symlinks=False,
            token=HF_TOKEN
        )
        print("✅ Text Encoder downloaded!")
    except Exception as e:
        print(f"❌ Error downloading Text Encoder: {e}")

    # 3. Download VAE
    print("\n📦 Downloading VAE (qwen_image_vae.safetensors)...")
    vae_dir = BASE_DIR / "vae"
    vae_dir.mkdir(parents=True, exist_ok=True)
    try:
        hf_hub_download(
            repo_id="Comfy-Org/Qwen-Image_ComfyUI",
            filename="split_files/vae/qwen_image_vae.safetensors",
            local_dir=str(vae_dir),
            local_dir_use_symlinks=False,
            token=HF_TOKEN
        )
        print("✅ VAE downloaded!")
    except Exception as e:
        print(f"❌ Error downloading VAE: {e}")

    # 4. Download Lightning LoRA (8-step bf16 version)
    print("\n📦 Downloading Lightning LoRA (Qwen-Image-Lightning-8steps-V2.0-bf16.safetensors)...")
    loras_dir = BASE_DIR / "loras"
    loras_dir.mkdir(parents=True, exist_ok=True)
    try:
        hf_hub_download(
            repo_id="lightx2v/Qwen-Image-Lightning",
            filename="Qwen-Image-Lightning-8steps-V2.0-bf16.safetensors",
            local_dir=str(loras_dir),
            local_dir_use_symlinks=False,
            token=HF_TOKEN
        )
        print("✅ Lightning LoRA downloaded!")
    except Exception as e:
        print(f"❌ Error downloading LoRA: {e}")

    print("\n🎉 All downloads complete!")
    print("\n📁 Model locations:")
    print(f"  - UNET: {unet_dir}")
    print(f"  - Text Encoder: {text_encoder_dir}")
    print(f"  - VAE: {vae_dir}")
    print(f"  - LoRAs: {loras_dir}")
    print("\n⚠️  Note: The UNET model (40GB) will take the longest to download")

if __name__ == "__main__":
    download_models()
