# ComfyUI Workflows Analysis & Integration Guide

## Overview

You have two powerful ComfyUI workflows on your RunPod instance for batch image processing using **Qwen Image Edit 2509** model. These workflows complement your NanaBanana/Gemini API workflow but serve different purposes.

---

## 🔄 Workflow Comparison

### **Workflow 3: Batch Models (Multiple Images → One Pose)**

**Title:** "OpenPose Workflow 3 - Group of images - Jockerai"

**Purpose:** Apply one specific pose to multiple different model images

**Input:**
- **Multiple model images** (loaded from folder via LoadImageListFromDir)
- **One pose reference image** (LoadImage node)

**Output:** All input images transformed to match the reference pose

**Example Use Case:**
- You have 100 different photos of Madison Morgan
- You have 1 perfect pose reference (e.g., hand on hip, looking over shoulder)
- Output: All 100 photos with that same pose

**Folder Configuration:**
```
Node 196 (easy string): "F:\youtube\OpenPose Qwen edit plus\images"
Node 179 (LoadImage): Single pose reference image
```

---

### **Workflow 4: Batch Poses (One Image → Multiple Poses)**

**Title:** "OpenPose Workflow 4 - Group of poses - Jockerai"

**Purpose:** Apply multiple different poses to one model image

**Input:**
- **One model image** (LoadImage node)
- **Multiple pose reference images** (loaded from folder via LoadImageListFromDir)

**Output:** The same model with multiple different poses

**Example Use Case:**
- You have 1 perfect photo of Madison Morgan (good lighting, expression, bikini)
- You have 20 different pose references
- Output: 20 variations of that photo with different poses

**Folder Configuration:**
```
Node 199 (easy string): "F:\youtube\OpenPose Qwen edit plus\pose images"
Node 200 (LoadImage): Single model image
```

---

## 🤖 Technical Details

### **Shared Configuration:**

**Model Stack:**
- **Main Model:** Qwen Image Edit 2509 (bf16) - `qwen_image_edit_2509_bf16.safetensors`
- **Text Encoder:** Qwen 2.5 VL 7B (fp8) - `qwen_2.5_vl_7b_fp8_scaled.safetensors`
- **VAE:** Qwen Image VAE - `qwen_image_vae.safetensors`
- **LoRA:** Qwen Image Lightning 8-steps V2.0 (for fast generation)

**Generation Settings:**
- **Steps:** 8 (fast generation thanks to Lightning LoRA)
- **Sampler:** euler_ancestral
- **CFG:** 1.0
- **Denoise:** 0.97
- **Scheduler:** normal

**Prompt:**
```
"the woman in image 1 has the pose in image 2. nude nail color"
```

### **Key Nodes:**

1. **LoadImageListFromDir //Inspire** - Batch loads images from a folder
2. **TextEncodeQwenImageEditPlus** - Special text encoder that accepts image references
3. **ImageScaleToTotalPixels** - Scales images to 1.1 megapixels (optimal for model)
4. **KSampler** - Main generation node
5. **SaveImage** - Saves outputs to ComfyUI output folder

---

## 🆚 NanaBanana API vs ComfyUI Workflows

### **NanaBanana/Gemini API**

**Best For:**
- ✅ Background replacement (Waikiki Beach, Lanikai Beach, etc.)
- ✅ Clothing changes (bikini styles, team jerseys)
- ✅ Scene modifications (adding people, surfers, palm trees)
- ✅ Photographic style control (f-stops, depth of field)
- ✅ Cloud-based (no GPU needed)

**Limitations:**
- ❌ Cannot do pose transfer
- ❌ Not ideal for batch processing (API rate limits)
- ❌ Costs per image ($0.134 for 2K)
- ❌ Processing time: ~30-60 seconds per image

**Cost:** $0.134 per 2K image (via Google API)

---

### **ComfyUI Workflows (Qwen Image Edit)**

**Best For:**
- ✅ Pose transfer (copy pose from one image to another)
- ✅ Batch processing (process 100+ images in one run)
- ✅ Consistent generation (same model, same settings)
- ✅ Local GPU control (no API limits)
- ✅ Fast generation (8 steps = ~5-10 seconds per image)

**Limitations:**
- ❌ Not ideal for background replacement (worse than Gemini)
- ❌ Not ideal for clothing changes (less precise than Gemini)
- ❌ Requires GPU (RunPod costs)
- ❌ No photographic control (f-stops, depth of field)

**Cost:** RunPod GPU rental (~$0.50-1.00/hour for RTX 4090)

---

## 🎯 Recommended Hybrid Workflow

### **Strategy: Use Both Systems for Optimal Results**

### **Phase 1: NanaBanana API for Hero Image Creation**

Use NanaBanana to create your "hero images" with perfect backgrounds and bikinis:

1. **Select 5-10 best Madison Morgan photos** from Instagram
2. **Generate variations with NanaBanana:**
   - Different Hawaiian beach backgrounds (Waikiki, Lanikai, Sunset Beach, etc.)
   - Different bikini styles (white triangle, floral, sporty, Saints/LSU themed)
   - Mix of sharp and blurry backgrounds
3. **Pick the best 3-5 results** as your "hero images"

**Cost:** ~$2-3 for 20-30 variations

---

### **Phase 2: ComfyUI for Pose Variation Batch**

Use ComfyUI Workflow 4 to create many pose variations from your hero images:

1. **Upload hero images to RunPod** (the best backgrounds + bikinis from Phase 1)
2. **Collect 20-30 pose references** (from other Instagram models, stock photos, etc.)
3. **Run Workflow 4** for each hero image against all pose references
4. **Result:** 3 hero images × 20 poses = 60 variations

**Cost:** ~$1-2 for 1-2 hours of GPU time

---

### **Phase 3: Curate and Post**

1. **Review all variations** (60+ images)
2. **Pick best 5-10 per carousel post**
3. **Optional:** Run favorites through NanaBanana again for final polish

---

## 📝 Step-by-Step: Using ComfyUI Workflows

### **Option A: Use Workflow 3 (Batch Models)**

**When to use:** You have many model images and want to apply one consistent pose

**Steps:**

1. **Prepare images on RunPod:**
```bash
ssh root@149.36.1.167 -p 13083 -i ~/.ssh/id_ed25519
mkdir -p /workspace/madison-morgan/input_images
mkdir -p /workspace/madison-morgan/pose_references
```

2. **Upload model images:**
```bash
# From local machine:
scp -P 13083 -i ~/.ssh/id_ed25519 /path/to/madison/*.jpg root@149.36.1.167:/workspace/madison-morgan/input_images/
```

3. **Upload one pose reference:**
```bash
scp -P 13083 -i ~/.ssh/id_ed25519 /path/to/pose.jpg root@149.36.1.167:/workspace/madison-morgan/pose_references/
```

4. **Open ComfyUI** (usually at http://149.36.1.167:8188)

5. **Load Workflow 3:**
   - Load `/workspace/ComfyUI/user/default/workflows/workflow_3_batch_models.json`

6. **Configure inputs:**
   - **Node 196 (easy string):** Set path to `/workspace/madison-morgan/input_images`
   - **Node 179 (LoadImage):** Select pose reference from `/workspace/madison-morgan/pose_references/`

7. **Modify prompt (Node 163):**
```
"the woman in image 1 has the pose in image 2. wearing a vibrant tropical floral bikini, Waikiki Beach background, professional beach photography"
```

8. **Run workflow** (Queue Prompt button)

9. **Download results:**
```bash
# Results saved to: /workspace/ComfyUI/output/
scp -P 13083 -i ~/.ssh/id_ed25519 -r root@149.36.1.167:/workspace/ComfyUI/output/* ./outputs/
```

---

### **Option B: Use Workflow 4 (Batch Poses)**

**When to use:** You have one hero image and want to apply many different poses

**Steps:**

1. **Prepare images on RunPod:**
```bash
ssh root@149.36.1.167 -p 13083 -i ~/.ssh/id_ed25519
mkdir -p /workspace/madison-morgan/hero_images
mkdir -p /workspace/madison-morgan/pose_library
```

2. **Upload one hero image:**
```bash
scp -P 13083 -i ~/.ssh/id_ed25519 hero_image.jpg root@149.36.1.167:/workspace/madison-morgan/hero_images/
```

3. **Upload multiple pose references:**
```bash
scp -P 13083 -i ~/.ssh/id_ed25519 /path/to/poses/*.jpg root@149.36.1.167:/workspace/madison-morgan/pose_library/
```

4. **Load Workflow 4:**
   - Load `/workspace/ComfyUI/user/default/workflows/workflow_4_batch_poses.json`

5. **Configure inputs:**
   - **Node 200 (LoadImage):** Select hero image from `/workspace/madison-morgan/hero_images/`
   - **Node 199 (easy string):** Set path to `/workspace/madison-morgan/pose_library`

6. **Modify prompt (Node 163):**
```
"the woman in image 1 has the pose in image 2. nude nail color, maintain bikini style and background"
```

7. **Run workflow** (Queue Prompt button)

8. **Download results** from `/workspace/ComfyUI/output/`

---

## 🎨 Prompt Engineering for ComfyUI

### **Basic Structure:**

```
"the woman in image 1 has the pose in image 2. [ADDITIONAL_DETAILS]"
```

### **Examples:**

**Preserve everything except pose:**
```
"the woman in image 1 has the pose in image 2. maintain exact outfit, background, and lighting"
```

**Specify details:**
```
"the woman in image 1 has the pose in image 2. wearing white triangle bikini, Lanikai Beach background, golden hour lighting, nude nail color"
```

**Sports theme:**
```
"the woman in image 1 has the pose in image 2. wearing New Orleans Saints themed bikini with black and gold colors, professional sports photography"
```

---

## 💰 Cost Comparison

### **Scenario: Create 100 Instagram carousel images**

#### **Option 1: NanaBanana API Only**
- 100 images × $0.134 = **$13.40**
- Time: ~50-100 minutes (sequential processing)
- Quality: Excellent backgrounds and clothing

#### **Option 2: ComfyUI Only**
- RunPod RTX 4090: ~$0.69/hour
- Generation: ~10 seconds per image = 17 minutes
- **Cost: ~$0.20**
- Quality: Excellent poses, but backgrounds not as good

#### **Option 3: Hybrid Approach (RECOMMENDED)**
- Phase 1: Generate 5 hero images with NanaBanana = **$0.67**
- Phase 2: Generate 100 pose variations on ComfyUI = **$0.50**
- **Total: ~$1.17**
- Quality: Best of both worlds
- Time: ~2 hours total

---

## 🚀 Quick Start Commands

### **Check if models are installed on RunPod:**

```bash
ssh root@149.36.1.167 -p 13083 -i ~/.ssh/id_ed25519

# Check UNET models
ls -lh /workspace/ComfyUI/models/unet/

# Check text encoders
ls -lh /workspace/ComfyUI/models/text_encoders/

# Check VAE
ls -lh /workspace/ComfyUI/models/vae/

# Check LoRAs
ls -lh /workspace/ComfyUI/models/loras/
```

**Expected files:**
- `qwen_image_edit_2509_bf16.safetensors` (UNET)
- `qwen_2.5_vl_7b_fp8_scaled.safetensors` (Text Encoder)
- `qwen_image_vae.safetensors` (VAE)
- `Qwen-Image-Lightning-8steps-V2.0-bf16.safetensors` (LoRA)

---

## 📊 Workflow Decision Tree

```
Do you need to change backgrounds or clothing?
├── YES → Use NanaBanana API
│   ├── Sharp background needed? → Use f/11, 24mm prompts
│   └── Blurry background needed? → Use f/2.8, 50mm prompts
│
└── NO → Do you need to change poses?
    ├── YES → Use ComfyUI Workflows
    │   ├── Many images, one pose → Workflow 3
    │   └── One image, many poses → Workflow 4
    │
    └── NO → You're done!
```

---

## 🔧 Troubleshooting

### **ComfyUI errors:**

**"Model not found"**
- Check model paths in nodes match actual file locations
- Verify all 4 models are downloaded (UNET, CLIP, VAE, LoRA)

**"Out of memory"**
- Reduce ImageScaleToTotalPixels multiplier from 1.1 to 1.0
- Process fewer images at once
- Use GGUF quantized models (lower quality, less VRAM)

**"Generation takes too long"**
- Increase steps from 8 to 12 for better quality
- Or decrease to 4-6 for faster generation
- Check Lightning LoRA is enabled and strength is 1.0

---

## 📚 Next Steps

1. **Test Workflow 4** with one hero image + 5 pose references
2. **Review quality** - is pose transfer accurate?
3. **If good:** Scale up to full batch
4. **If not:** Try NanaBanana API for everything (slower but more reliable)

---

## 🎯 Final Recommendation

**For your Madison Morgan use case:**

1. ✅ Use **NanaBanana API** for initial hero images (backgrounds + bikinis)
2. ✅ Use **ComfyUI Workflow 4** to create pose variations if needed
3. ✅ Combine outputs for maximum carousel content
4. ✅ Curate best results for each post

This gives you the best quality-to-cost ratio and maximum creative control.
