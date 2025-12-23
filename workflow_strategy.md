# Content Generation Strategy: NanaBanana vs ComfyUI Workflows

## Current Data Inventory

### Instagram Data (Source Content)
- **ISMÊ**: 874 posts, 2,762 images ✅
- **Jade Swim**: No Instagram data ❌
- **Midori Bikinis**: No Instagram data ❌
- **Vitamin A**: No Instagram data ❌

### Product Catalogs (Bikini Swap Library)
- **ISMÊ**: 128 products, 985 images
- **Jade Swim**: 156 products, 1,235 images
- **Midori Bikinis**: 77 products, 170 images
- **Vitamin A**: 250 products, 1,155 images

**Total**: 611 products, 3,545 product images

---

## Your Goal

**Input**: Influencer Instagram images (bikini content)
**Transformations**:
1. Swap bikini → Your brand's bikinis (ISMÊ, Jade Swim, etc.)
2. Change background → Different beach/pool/yacht locations
3. Face swap → AI model faces

**Output**: Legally distinct AI influencer content for Instagram/FanView

---

## Tool Comparison: NanaBanana vs ComfyUI

### NanaBanana (Gemini Nano Banana Pro)

**Pros**:
- ✅ Simple API calls ($0.25/edit)
- ✅ Fast for testing
- ✅ No GPU setup needed
- ✅ Good for rough drafts

**Cons**:
- ❌ Costs add up (10,000 edits = $2,500)
- ❌ Less precision than ComfyUI
- ❌ Face changes slightly
- ❌ Quality loss in details
- ❌ No mask-based control

**Best Use Cases**:
- Quick proof-of-concept tests
- When RunPod is down
- Simple edits that don't need perfect precision

---

### ComfyUI Workflows (QWen Image Edit Plus 259)

**Pros**:
- ✅ FREE (only RunPod GPU cost ~$0.50/hr)
- ✅ 100% subject preservation (face, skin, details)
- ✅ Mask-based editing (surgical precision)
- ✅ Perfect for batch processing
- ✅ Professional quality output
- ✅ Lightning LoRA = 8 steps (fast generation)

**Cons**:
- ❌ Requires GPU setup on RunPod
- ❌ Steeper learning curve
- ❌ Need to download models (40GB)

**Best Use Cases**:
- Production content generation
- High-volume batch processing
- When precision matters (face must stay same)
- Professional quality output

---

## Recommended Workflow for Your Use Case

### Phase 1: Setup (One-Time)

**On RunPod** (pod dztg0x5jg2o9cd):
1. Download QWen Image Edit Plus 259 model (FP8 version for 24GB GPU)
2. Download LoRAs:
   - Lightning LoRA (8-step speedup)
   - Fusion LoRA (for bikini swapping)
   - White-to-Scene LoRA (for background changes)
3. Import ComfyUI workflows (you already have the JSON files)

**Locally**:
1. Scrape Instagram from other brands (Jade Swim, Midori, Vitamin A)
2. Organize influencer content by engagement score

---

### Phase 2: Content Pipeline (Use ComfyUI)

```
STEP 1: Select Source Image
├─ Choose high-engagement Instagram post from ISMÊ (or other brand)
├─ Ideally: bikini content with clean background
└─ Save to input folder

STEP 2: Bikini Swap (ComfyUI Workflow 2 - Put On Any Clothes V5)
├─ Load source image
├─ Load product image from your brand catalog
├─ Open Mask Editor → Paint bikini area
├─ Prompt: "This woman in image 1 is wearing the bikini in image 2"
├─ Generate (8 steps with Lightning LoRA)
└─ Output: Same pose/face, new bikini

STEP 3: Background Change (ComfyUI Workflow 1 - Change Background V2)
├─ Load bikini-swapped image from Step 2
├─ Remove background node strips white background
├─ Prompt: "This woman on a beach in Santorini Greece with white buildings"
├─ Generate (8 steps)
└─ Output: New background, perfect lighting

STEP 4: Face Swap (Replicate API)
├─ Use your Replicate API token (from .env)
├─ Swap face to your AI model's face
└─ Output: Legally distinct content

STEP 5: Quality Check & Post
├─ Review for artifacts
├─ Schedule to Instagram/FanView
└─ Track engagement
```

---

### Phase 3: Batch Scaling

**Content Multiplication Formula**:
```
1 source image × 10 bikinis × 5 backgrounds × 3 faces = 150 variations
```

**Efficiency**:
- ComfyUI on RTX 4090: ~10-15 seconds per image (8 steps)
- 150 variations = ~30-40 minutes of GPU time
- Cost: $0.50/hr GPU = ~$0.30 total
- NanaBanana equivalent: 150 × $0.25 = **$37.50**

**Savings**: $37.20 per batch (124x cheaper)

---

## When to Use Each Tool

### Use ComfyUI When:
- ✅ Generating production content at scale
- ✅ Need 100% face preservation before face swap
- ✅ Want professional quality for Instagram
- ✅ Processing 10+ images per session
- ✅ Budget matters (high volume)

### Use NanaBanana When:
- ✅ Testing a single concept quickly
- ✅ Don't have access to RunPod temporarily
- ✅ Need a rough draft for client approval
- ✅ Editing 1-5 images only

---

## Missing Data: Instagram Scraping Needed

You currently **only have Instagram data from ISMÊ**. To expand content sources, scrape:

### Priority Brands to Scrape:
1. **Jade Swim** (@jadeswim)
   - Luxury bikini brand
   - High-quality lifestyle content
   - 156 products ready for swapping

2. **Midori Bikinis** (@midoribikinis)
   - Sporty bikini aesthetic
   - 77 products

3. **Vitamin A** (@vitaminaswim)
   - Established brand
   - 250 products (largest catalog)

### How to Scrape:
```bash
# Use your existing Apify script
node scripts/scrape_brand_instagram.js jade-swim
node scripts/scrape_brand_instagram.js midori-bikinis
node scripts/scrape_brand_instagram.js vitamin-a
```

---

## Workflow Files You Have

### ComfyUI Workflows (In Root Directory):
1. ✅ `Put On Any Clothes V5 wokflow 2- Jockerai.json`
   - **USE THIS**: Mask-based bikini swapping
   - Face preservation: 100%

2. ✅ `Put On Any Clothes V5 (GGUF) workflow 2 - Jockerai.json`
   - Same as above, but for weaker GPUs (16GB VRAM)

3. ✅ `Change Background V2 - Jockerai.json`
   - **USE THIS**: Background replacement
   - Subject preservation: 100%

4. ✅ `Put Any Subject in V2 - Jockerai.json`
   - For blending Photoshop composites
   - Less relevant for your use case

### Documentation:
- ✅ `comfyui_workflows_guide.md` - Strategic guide I created
- ✅ `comfyui_video_transcripts.md` - Raw video transcripts

---

## Recommended Next Steps

### Immediate (This Week):
1. **SSH into RunPod** and verify ComfyUI installation
2. **Download models** (QWen 259 FP8, Lightning/Fusion/White-to-Scene LoRAs)
3. **Test Workflow 2** with 1 ISMÊ Instagram image + 1 ISMÊ product
4. **Test Workflow 1** with output from step 3
5. **Test face swap** with Replicate API

### Short-Term (Next 2 Weeks):
1. **Scrape Instagram** from Jade Swim, Midori, Vitamin A
2. **Process top 10 posts** from each brand (40 total)
3. **Generate 5 bikini variations** per post (200 images)
4. **Generate 3 background variations** per bikini (600 images)
5. **Face swap all 600** → Final content library

### Long-Term (Scale):
1. **Automate pipeline** with Python script
2. **Schedule content** to Instagram (2-3 posts/day)
3. **Track engagement** to identify top performers
4. **Expand to more brands** (10+ swimwear brands)
5. **Pitch brand partnerships** with your content library as proof

---

## Cost Comparison: Full Pipeline

### NanaBanana Route:
```
1,000 bikini swaps × $0.25 = $250
1,000 background changes × $0.25 = $250
1,000 face swaps × $0.25 = $250
TOTAL: $750
```

### ComfyUI Route:
```
RunPod RTX 4090: $0.50/hr
Generation time: 10 seconds/image
1,000 images = 10,000 seconds = 2.8 hours
GPU cost: $1.40
Face swap API: 1,000 × $0.01 = $10
TOTAL: $11.40
```

**Savings**: $738.60 (65x cheaper)

---

## Summary

**For Your Bikini Content Machine**:
- ✅ **Use ComfyUI Workflow 2** for all bikini swaps
- ✅ **Use ComfyUI Workflow 1** for all background changes
- ✅ **Use Replicate API** for face swaps
- ❌ **Skip NanaBanana** unless testing quick concepts

**Why ComfyUI Wins**:
1. 100% face preservation (critical before face swap)
2. Professional quality for Instagram
3. 65x cheaper at scale
4. Perfect for batch processing

**What You're Missing**:
- Instagram data for Jade Swim, Midori Bikinis, Vitamin A
- Need to scrape these to expand content sources beyond ISMÊ

**Your Advantage**:
- 611 products ready to swap
- 2,762 ISMÊ Instagram images ready to transform
- Workflows already downloaded and ready
- Clear content multiplication path (1 → 150 variations)
