# Gemini Image Editing Prompting Guide
*Complete guide for background replacement and image editing with NanaBanana Pro / Gemini*

---

## 🎯 Core Principle

**Be explicit about what you want!** Gemini follows instructions literally, so specify:
- What to change (background, clothing, etc.)
- What to keep (pose, expression, face)
- How the final image should look (style, focus, mood)

---

## 📸 Camera Settings & Focus Control

### **Sharp Background (Landscape Style)**
Use when you want the location to be recognizable and clear.

```
Shot with 24mm wide-angle lens, f/11, deep depth of field.
Everything in sharp focus from foreground to background.
Professional landscape travel photography.
Sharp focus throughout the entire image.
```

**Best for:**
- Iconic locations (Diamond Head, Mokulua Islands, landmarks)
- Showcasing specific beaches
- Travel/destination content
- When the background tells the story

**Result:** Beach features clearly visible and recognizable

---

### **Blurry Background (Portrait Style)**
Use when you want subject to stand out with dreamy background.

```
Shot with 50mm lens, f/2.8, shallow depth of field.
Dreamy bokeh background blur.
Professional portrait photography style.
Subject in sharp focus, background softly blurred.
```

**Best for:**
- Emphasizing the model
- Artistic/editorial style
- When background is just atmosphere
- More intimate, focused feel

**Result:** Subject pops, background is soft and dreamy

---

### **Balanced Approach (Moderate)**
Use when you want both subject and background visible.

```
Shot with 35mm lens, f/5.6, moderate depth of field.
Subject sharp with clear visible background landmarks.
Professional travel photography, balanced composition.
```

**Best for:**
- Balanced travel content
- When both model and location matter equally
- Commercial/advertising style

**Result:** Both subject and location are clear but subject still stands out

---

## 🏖️ Beach Background Elements

### **Empty Beach (Serene)**
```
Pristine empty beach, no people visible.
Peaceful and serene atmosphere.
Private paradise feel.
```

**Effect:** Exclusive, romantic, tranquil vibe

---

### **Beach with People (Lively)**
```
Surfers in the distance riding waves.
Beachgoers and tourists walking on the sand.
Active beach atmosphere with people.
```

**Effect:** Dynamic, social, authentic travel feel

**Tip:** Use "in the distance" or "background" to keep people small and not distracting

---

### **Golden Hour vs Midday**

**Golden Hour (Sunrise/Sunset):**
```
Warm golden hour sunlight, soft morning/evening light.
Vibrant orange and pink sunset sky.
Warm glow on skin and sand.
```
**Effect:** Romantic, dreamy, Instagram-worthy

**Midday (Bright & Clear):**
```
Bright sunny midday light, clear blue sky.
Vibrant colors, high contrast.
Professional daytime photography.
```
**Effect:** Energetic, vibrant, classic beach day

---

## 👙 Clothing Changes

### **Specific Clothing Instructions**

Always be VERY specific about clothing:

```
Change her bikini to [COLOR] [STYLE] [DETAILS].
```

**Examples:**

**Classic/Simple:**
```
Change her bikini to a classic white triangle bikini.
Change her bikini to a sleek black sporty athletic bikini.
```

**Patterned:**
```
Change her bikini to a vibrant tropical floral print bikini with hibiscus flowers.
Change her bikini to a navy blue and white striped bikini.
```

**Sports Team Themed:**
```
Change her bikini to a black and gold New Orleans Saints themed bikini
with subtle fleur-de-lis symbols and gold metallic accents.

Change her bikini to a purple and gold LSU Tigers themed bikini
with tiger stripe pattern and team colors.
```

**Tip:** Add texture/material details for more realistic results:
- "metallic gold accents"
- "ribbed fabric texture"
- "subtle shine finish"

---

## 🎨 Complete Prompt Template

### **Full Prompt Structure:**

```
[ACTION] Replace the background with [LOCATION].
[CLOTHING] Change her [ITEM] to [SPECIFIC DESCRIPTION].
[CAMERA] Shot with [LENS]mm lens, f/[APERTURE], [DEPTH OF FIELD].
[SCENE DETAILS] [Specific landmarks, features, elements].
[LIGHTING] [Time of day, light quality, atmosphere].
[STYLE] Professional [PHOTOGRAPHY TYPE] style.
[FOCUS] [Sharp/blurred background instruction].
[PRESERVE] Keep her pose and expression unchanged, only modify [WHAT YOU'RE CHANGING] seamlessly.
```

---

## 📋 Example Prompts

### **Example 1: Sharp Landscape Beach**
```
Replace the background with Lanikai Beach in Oahu, Hawaii.
Change her bikini to a vibrant tropical floral print bikini with hibiscus flowers.
Shot with 24mm wide-angle lens, f/11, deep depth of field.
The iconic Mokulua twin islands clearly visible in crystal clear turquoise water,
powdery white sand beach, lush tropical palm trees.
Soft morning golden light, professional landscape travel photography.
Sharp focus throughout the entire image from foreground to background.
Keep her pose and expression unchanged, only modify background and bikini seamlessly.
```

---

### **Example 2: Blurry Portrait Style**
```
Replace the background with Malibu Beach in California.
Change her bikini to a classic black triangle bikini.
Shot with 85mm portrait lens, f/2.8, shallow depth of field.
Golden sand, ocean waves, palm trees in soft focus.
Warm golden hour sunset light, professional portrait photography.
Dreamy bokeh background, subject in sharp focus.
Keep her pose and expression unchanged, only modify background and bikini seamlessly.
```

---

### **Example 3: Sports Team Bikini**
```
Replace the background with Miami South Beach.
Change her bikini to a Miami Dolphins themed bikini with aqua and orange team colors,
subtle dolphin logo pattern, athletic sporty cut with metallic accents.
Shot with 35mm lens, f/5.6, moderate depth of field.
Art deco buildings visible in background, turquoise ocean, white sand.
Bright sunny midday light, vibrant Miami atmosphere.
Subject sharp with clear visible background landmarks.
Keep her pose and expression unchanged, only modify background and bikini seamlessly.
```

---

## ⚙️ Resolution & Quality Settings

### **Resolution Options:**
- **1K**: 1024px (basic quality)
- **2K**: 2048px (recommended - same price as 1K!)
- **4K**: 4096px (2x cost, best for hero images)

### **Cost Comparison:**
| Resolution | Google API | Batch API | Use Case |
|------------|-----------|-----------|----------|
| 1K | $0.134 | $0.067 | Legacy/testing |
| 2K | $0.134 | $0.067 | Standard (recommended) |
| 4K | $0.240 | $0.120 | Hero/print quality |

**Recommendation:** Always use 2K minimum (same cost as 1K, better quality)

---

## 🎭 Style Variations

### **Travel Photography**
```
Professional travel photography, National Geographic style.
```
**Effect:** Editorial, magazine quality, polished

### **Editorial Fashion**
```
Editorial fashion photography, Vogue style, high fashion.
```
**Effect:** Sophisticated, artistic, high-end

### **Lifestyle/Candid**
```
Natural lifestyle photography, candid moment, authentic feel.
```
**Effect:** Relatable, real, unposed vibe

### **Commercial/Advertising**
```
Commercial advertising photography, vibrant and eye-catching.
```
**Effect:** Bold colors, perfect lighting, product-focused

---

## 🚫 Common Mistakes to Avoid

### **❌ Don't:**
1. Use vague descriptions: "nice beach" → ❌
2. Contradict yourself: "sharp focus" + "bokeh blur" → ❌
3. Over-complicate: Keep one clear goal per edit
4. Forget to preserve: Always say what to keep unchanged
5. Mix styles: Choose one photography style

### **✅ Do:**
1. Be specific: "Waikiki Beach with Diamond Head crater" → ✅
2. Be consistent: Choose sharp OR blurry, not both
3. Focus on one change: Background OR clothing, then iterate
4. Explicitly preserve: "Keep pose and expression unchanged"
5. Use photographic terms: f-stops, lens types, etc.

---

## 🎯 Quick Reference

### **For Sharp Backgrounds:**
- 24mm wide-angle
- f/11
- "deep depth of field"
- "sharp focus throughout"

### **For Blurry Backgrounds:**
- 50-85mm lens
- f/2.8
- "shallow depth of field"
- "bokeh background blur"

### **For Balance:**
- 35mm lens
- f/5.6
- "moderate depth of field"
- "balanced composition"

---

## 💡 Pro Tips

1. **Test variations:** Generate 2-3 versions with different settings
2. **Iterate:** Use the best result and refine with follow-up edits
3. **Reference real photos:** Look at actual beach photography for inspiration
4. **Use 2K resolution:** It's the same price as 1K
5. **Save good prompts:** Build a library of proven prompts
6. **Be patient:** Complex edits take 30-60 seconds
7. **Specificity wins:** More details = better results

---

## 📚 Resources

- [Google Gemini Image Generation Tips](https://blog.google/products/gemini/image-generation-prompting-tips/)
- [Imagen 3 Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/image/img-gen-prompt-guide)
- [NanaBanana Pro Pricing](https://www.nano-banana.ai/pricing)

---

## 🔄 Version History

- **v1.0** - Initial guide (Dec 2025)
  - Sharp vs blurry backgrounds
  - Clothing changes
  - Sports team bikinis
  - Complete prompt templates
