#!/bin/bash
# Model download script for Qwen Image Edit workflows
# Optimized for RTX 5090 (32GB VRAM) - downloading bf16 versions

set -e

echo "=========================================="
echo "Downloading Qwen Image Edit Models"
echo "Target: RunPod instance at 149.36.1.167"
echo "=========================================="

# SSH connection details
SSH_HOST="root@149.36.1.167"
SSH_PORT="13083"
SSH_KEY="~/.ssh/id_ed25519"
COMFY_PATH="/workspace/ComfyUI/models"

echo ""
echo "1/4 Downloading Text Encoder (~15GB)..."
ssh -p $SSH_PORT -i $SSH_KEY $SSH_HOST "cd $COMFY_PATH/text_encoders && wget -c https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors"

echo ""
echo "2/4 Downloading VAE (~2GB)..."
ssh -p $SSH_PORT -i $SSH_KEY $SSH_HOST "cd $COMFY_PATH/vae && wget -c https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors"

echo ""
echo "3/4 Downloading Main UNET Model bf16 (~40GB)..."
ssh -p $SSH_PORT -i $SSH_KEY $SSH_HOST "cd $COMFY_PATH/unet && wget -c https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_edit_2509_bf16_3.safetensors"

echo ""
echo "4/4 Downloading Lightning LoRA bf16 (~500MB)..."
ssh -p $SSH_PORT -i $SSH_KEY $SSH_HOST "cd $COMFY_PATH/loras && wget -c https://huggingface.co/lightx2v/Qwen-Image-Lightning/resolve/main/Qwen-Image-Lightning-8steps-V2.0-bf16.safetensors"

echo ""
echo "=========================================="
echo "Download Complete!"
echo "=========================================="
echo ""
echo "Verifying downloads..."
ssh -p $SSH_PORT -i $SSH_KEY $SSH_HOST "ls -lh $COMFY_PATH/text_encoders/*.safetensors && ls -lh $COMFY_PATH/vae/*.safetensors && ls -lh $COMFY_PATH/unet/*.safetensors && ls -lh $COMFY_PATH/loras/*.safetensors"

echo ""
echo "All models downloaded successfully!"
echo "Total size: ~57GB"
