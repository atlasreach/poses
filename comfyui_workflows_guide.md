# ComfyUI QWen Image Edit Plus Workflows Guide

## Overview
Two powerful ComfyUI workflows using **QWen Image Edit Plus** for precise image editing:
1. **Change Background V2** - Replace backgrounds while preserving product/subject 100%
2. **Put On Any Clothes V5** - Change outfits with 10x more accuracy than previous versions

---

## Workflow 1: Change Background V2

### What It Does
- Replaces image backgrounds while keeping subject **completely unchanged**
- Preserves textures, reflections, text, labels, and tiny details
- Automatic lighting and color matching
- Perfect for product photography

### Key Features
- **100% Subject Preservation** - No distortion, texture loss, or shifted proportions
- **Two Modes:**
  - **Mode A:** Generate background from text prompt
  - **Mode B:** Place subject into existing background image

### Requirements
**Models:**
- QWen Image Edit Plus 259 (40GB) or FP8 version (20GB)
- Text Encoder model
- VAE model
- Lightning LoRA (8-step version)
- **White-to-Scene LoRA** - Key component for background replacement

**GPU Requirements:**
- 32GB VRAM: Use original BF16 model
- 24GB VRAM: Use FP8 version
- 16GB VRAM: Use GGUF Q5 version
- 8GB VRAM: Use GGUF Q2 version

### How It Works

#### Mode A: Generate Background from Prompt
```
INPUT:
- Product image with white/transparent background
- Text prompt describing desired background

PROCESS:
1. Remove background node strips existing background
2. QWen Image Edit + White-to-Scene LoRA generates new background
3. Lighting LoRA speeds up generation (8 steps instead of 25)

OUTPUT:
- Product placed in new background
- Perfect lighting, shadows, reflections
- 100% product preservation
```

**Example Prompt:**
```
"This car on display at an indoor auto show surrounded by
spotlights and glossy reflections on polished floor"
```

#### Mode B: Place Subject in Existing Background
```
INPUT:
- Product images (with transparent background)
- Background image
- Products manually placed in Photoshop (no lighting/shadows needed)

PROCESS:
1. AI blends products into background
2. Corrects perspective automatically
3. Adds realistic lighting, shadows, reflections

OUTPUT:
- Seamlessly integrated scene
- Natural lighting and perspective
- Professional quality composite
```

**Example Prompt:**
```
"Blend the image, correct the products perspective and lighting,
and integrate the product into the background"
```

### Key Settings

**LoRA Strength Control:**
- `1.0` = Maximum precision (100% product preservation)
- `0.5` = Balanced (cinematic lighting + high precision)
- `0.3` = More cinematic (slight product changes acceptable)

**Important Notes:**
- **Trigger Word:** Chinese trigger word required (included in workflow)
- **Background Color:** Works best with white or simple backgrounds
- **Sampler:** Euler A recommended for best quality
- **Denoise:** 0.97 (not 1.0) for more natural lighting blend

---

## Workflow 2: Put On Any Clothes V5

### What It Does
- Changes clothing/outfits on subjects with extreme precision
- Can also apply accessories (necklaces, shoes, etc.)
- Preserves face, skin details, and image quality

### Two Workflow Versions

#### **Workflow 1 (Basic):**
- Edits entire photo based on prompt
- **Downside:** Slightly changes face and reduces quality
- Faster but less precise

#### **Workflow 2 (Advanced - RECOMMENDED):**
- **Mask-based editing** - Only edits areas you paint
- Face stays 100% unchanged
- Original image quality preserved
- No quality loss or unwanted changes

### How Workflow 2 Works (Mask-Based)

```
STEP 1: Prepare Images
- Subject image (person to change clothes on)
- Clothing image (product photo OR person wearing the outfit)

STEP 2: Create Mask
- Right-click subject image → "Open in Mask Editor"
- Paint over areas where clothing should appear
- Don't paint face, hair, or areas that won't be covered

STEP 3: Write Prompt
"This woman in image 1 is wearing the dress in image 2"

STEP 4: Generate
- AI only edits masked areas
- Everything else stays pixel-perfect
```

### Key Advantages of Workflow 2

✅ **Face Preservation** - Subject's face stays exactly the same
✅ **Quality Retention** - Original photo quality maintained
✅ **Skin Detail** - Pores, texture, makeup all preserved
✅ **No Shifting** - Subject doesn't move or change position
✅ **Precise Control** - Only edit what you mask

### Masking Strategy

**What to Mask:**
- Areas where clothing will cover
- Slightly larger than needed (give AI room to work)

**What NOT to Mask:**
- Face (unless changing hat/glasses)
- Exposed skin (arms, neck, chest if outfit doesn't cover)
- Background
- Hair (unless outfit has hood/hat)

**Example:**
```
Bikini Change:
- Mask: Chest, torso, hips (bikini coverage area)
- Don't mask: Face, arms, legs, background
```

### Requirements
**Same as Workflow 1:**
- QWen Image Edit Plus 259
- Lightning LoRA (8-step)
- **Fusion LoRA** (specific to clothing changes)

**Settings:**
- Steps: 8 (with Lightning LoRA)
- Sampler: Euler A
- Denoise: 0.97
- CFG Scale: As specified in workflow

---

## Strategic Recommendations for Your Bikini Project

### **WORKFLOW 1 (Background Change) - PRIMARY USE**

**Perfect For:**
- Taking Instagram bikini posts
- Changing backgrounds to different beaches/pools/yachts
- Creating location variations without pose changes

**Example Use Case:**
```
INPUT: Madison.moorgan turquoise bikini on Mediterranean beach
CHANGE TO: Same pose/bikini, but Miami South Beach background
RESULT: 1 post → 5 location variations
```

**How to Use:**
1. Select top 10 Instagram bikini posts
2. For each post, generate 5 different backgrounds:
   - Miami Beach
   - Santorini Greece
   - Ibiza Spain
   - Maldives
   - Private yacht
3. Result: 10 posts → 50 variations (just from backgrounds)

---

### **WORKFLOW 2 (Clothes Change) - CORE CONTENT ENGINE**

**Perfect For:**
- Swapping bikinis from your ISMÊ product library
- Testing different bikini colors/styles on same pose
- Brand-specific content creation

**Example Use Case:**
```
INPUT: Post with turquoise bikini on beach
BIKINI OPTIONS: 10 ISMÊ bikinis from library
RESULT: 1 post → 10 bikini variations
```

**How to Use:**
1. Take 1 high-performing Instagram post
2. Mask the bikini area
3. Swap in 10 different ISMÊ bikinis from library
4. Generate 10 versions
5. Combine with Workflow 1 for backgrounds
6. Result: 1 post × 10 bikinis × 5 backgrounds = **50 variations**

---

## **MY RECOMMENDED WORKFLOW FOR YOU:**

### **Phase 1: Pure Bikini Swaps (Fast Content)**
```
Step 1: Select 10 top Instagram posts (bikini content only)
Step 2: For each post:
   - Use Workflow 2 (mask bikini area)
   - Swap in 5 ISMÊ bikinis
   Result: 10 posts × 5 bikinis = 50 images

Step 3: Quality check + face swap
Step 4: Schedule to Instagram
```

**Time Estimate:** 2-3 hours for 50 images

---

### **Phase 2: Background Variations (2x Content)**
```
For top 5 performing posts from Phase 1:
   - Use Workflow 1 (background change)
   - Generate 3 location variations each
   Result: 5 posts × 3 backgrounds = 15 more images

Total from Phase 1 + 2: 65 images
```

---

### **Phase 3: Full Combinations (Massive Scale)**
```
Take top 3 posts:
   - 5 bikini swaps (Workflow 2)
   - 3 background changes per bikini (Workflow 1)
   Result: 3 posts × 5 bikinis × 3 backgrounds = 45 images

TOTAL: 110+ unique images from just 10 original posts
```

---

## **Technical Setup on RunPod:**

### **What You Need:**
1. ComfyUI installed on RunPod pod
2. QWen Image Edit Plus 259 model downloaded
3. Lightning LoRA + White-to-Scene LoRA (backgrounds)
4. Lightning LoRA + Fusion LoRA (clothing)
5. Both workflow JSON files

### **Recommended Pod:**
- GPU: RTX 4090 (24GB) or A6000 (48GB)
- Use FP8 model version for 24GB
- 8-step generation = very fast

---

## **Advantages Over NanaBanana:**

| Feature | NanaBanana | QWen ComfyUI |
|---------|-----------|--------------|
| **Cost** | $0.25/edit | Free (RunPod cost only) |
| **Precision** | Good | **Excellent** (100% preservation) |
| **Control** | Prompt-based | Mask-based control |
| **Batch** | One at a time | Batch processing |
| **Speed** | API wait time | Instant (on your GPU) |

---

## **Next Steps:**

1. **Get RunPod pod running** (you already have pod dztg0x5jg2o9cd)
2. **Install ComfyUI** (if not already installed)
3. **Download both workflows** from video descriptions
4. **Download models** (QWen 259, LoRAs)
5. **Test with 1 Instagram post:**
   - Try Workflow 2: swap 2-3 bikinis
   - Try Workflow 1: change background 2-3 times
6. **Scale up** once you confirm quality

---

## **Links to Videos:**
- Background Change V2: [YouTube link from transcript]
- Put On Clothes V5: [YouTube link from transcript]

---

## **Summary:**

**For Your Project:**
- **Workflow 2** = Your main content generator (bikini swaps)
- **Workflow 1** = 3x multiplier (background variations)
- **Together** = Exponential content from minimal source material

**Expected Output:**
- 10 Instagram posts → 100+ unique images
- Brand-specific (ISMÊ bikinis)
- Professional quality
- Ready for Instagram + FanView
