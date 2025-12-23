# ComfyUI QWen Image Edit Plus Video Transcripts

## Video 1: Put On Any Clothes Workflow V5

00:00:00
put any outfit on any subject, but this time with 10 times more accuracy and quality compared to workflow version 4. In this video, we are introducing version five of the put on any clothes workflow. Unlike the previous versions that work with Flux, this one uses the brand new Quinn image edit plus 259 model, an upgraded version of Quinn image edit with much higher precision. We have got two workflows in this video. Workflow one, when you give it a prompt, it edits the entire photo, including the

00:00:34
subject's face, areas you didn't want changed. Workflow one still touches the face slightly, altering the look and lowering overall image quality. Workflow two, this one only edits the areas you tell it to. It changes just those parts, leaving the face and background untouched. This makes a huge difference. The subject's face stays exactly the same. Skin details remain intact and the output photo keeps the same high quality as the original input. In workflow one, a lot of those details get lost. Now,

00:01:10
let's jump inside the workflow and I'd explain everything step by step. I really appreciate if you like the video right now and subscribe the channel for my next fantastic tutorials. First, you will need Comfy UI installed. If you haven't done that yet, check out my tutorial video where I go through the complete installation. This one in my channel. After that, download the workflows. Links are in the description. Workflow one is totally free and workflow 2 is exclusive for my W and

00:01:43
Boosty subscribers. Once you have downloaded the workflow, open Comfy UI. Go to manager and click on update all to bring your Comfy UI and all custom nodes to the latest version. Then restart the Comfy UI. Finally, just drag and drop the workflow into Comfy UI to start using it. After you download the workflows, you will receive these four files. The first two files are the workflow number one which I mentioned will edit the entire photo and the other two files are the workflow number two which can edit only the part that we

00:02:16
select. This is considered a big advantage to run them. It's enough to just drag and drop the workflow into your comfy UI. This one here is workflow number one. You can see that in this nodes you need to load your models. All the models you need I've written here for you. For example, for this node, you must download the main QN image edit 259 model. You can either use the lightweight version or the original full model. For the lightweight versions, which are the GGUF versions, you should

00:02:44
use workflow number one, GGUF version. But if you download the original QN model, then you must use workflow number one, original version. The GGUF version is for computers that are a bit weaker because these are the lighter versions of the QN model. If you want to download the original full model, you absolutely need a powerful GPU, 24 GB or 32 GB VRAM. Even with a 16 GB GPU, you can somehow use the original model, but the process of generating photos will become very slow. For these models, you simply

00:03:15
click on this button and start the download. It opens this page and here you see four models. The two at the bottom are not relevant. They are older QNageedit models. What we want is the new QN ImageEdit 259 model, which is the plus version of QN ImageEdit. You should download one of the top two. If your GPU has 32 GB VRAM or more, you can download the first one. But if you have 24 GB VRAM, you can use the second one, which is the FP8 version. Even on a 32 GB GPU, the first version runs a bit heavy

00:03:46
because it is 40 GB in size, which is larger than the VRAM capacity of your GPU. But your computer can also use some of your system RAM in order to load the model. Since I have 32 GB VRAM, I downloaded this model and placed it inside my workflow. Also, make sure to set this option to FP8 if you want your generation speed to be higher. But if you want the full quality, the maximum possible quality, you can set this option to default. In that case, it will use the full 40 GB. If you set it to the

00:04:15
second option, FP8, it will use half the size of the model. or you can directly download the FP8 version itself. And then it doesn't matter which of these two options you select because the model itself is FP8 by default and already compressed. The GGF version is downloaded from this link. When you go there, you'll see that it has different versions. For example, if you have an 8 GB GPU, you can use the Q2 model because its size is less than 8 GB. So, it won't put too much pressure on your GPU and

00:04:42
you can run this model, but the higher you go, the stronger GPU you need. For example, if you have a 16 GB GPU, you can use the Q5 version or Q5M, which is a little smaller than Q5L. If you have a 24 GB GPU, you can even use the Q8 version. This one here is the text encoder, and it goes here in this node. You download it from this link. This one is for the VAE. And this last option here is the Lightning Lura, which allows you to use eight steps instead of 20 steps. When I click on this to download

00:05:11
the Laura, you can see there are a few different versions of it. My suggestion is that you don't go for the four-step version and instead use the eight-step versions. In this section, you can see that we have different models for eight steps. If you downloaded the original Q&A image model BF-16, then your Laura should also be BF-16. But if you're using the GGF versions or FP8, then you should use the Laura versions that don't have BF-16 in their name. Here, I've explained clearly where each one should

00:05:38
be placed. Put each file into its own correct folder. Now here you can easily load each of these models. If the models you downloaded and placed in their folders don't show up in your comfy UI, just press the R key on your keyboard once and your Conf UI will refresh. After refreshing, the models will appear here. After you've downloaded everything, place them into their specific folders and hit R in confi. You still need to select each model one by one. Even if you see their names showing

00:06:04
up here, you must select them again. The same goes for the next nodes. Here you write your prompt. And here you can also use eight steps instead of 20 steps. Why? Because our Laura is active here. We also have an option called sampler name. If you click on it, you'll see many different samplers. Personally, I got much better results with Oiler A. Both the output quality is higher and the colors look much more natural. Of course, you can test the others yourself. This D noise setting here, I

00:06:29
set it to 0.97, while usually it's set to one. The reason for this is so that the output can borrow a little bit of the lighting and color from the reference image, giving us a more natural looking result. In these two sections, you must upload your model image and your clothing image. In the first node, I place the image of my model. And in the second node, I can either upload the product photo of the clothing or choose a clothing item that is already on another subject. Here, for example, I selected an image of a

00:06:56
subject wearing a piece of clothing. And in my prompt, I wrote, "This woman in image one is wearing the dress in image two." You can also give the AI more instructions by adding more sentences, but even this one sentence is enough. We also have a note here called scale image to total pixels. This ensures that your input image is resized to the megapixel value set here. If your input is larger, it scales it down close to 1.2 MP. And if it's smaller, it scales it up closer to this number. And finally, here we can

00:07:23
see the output image. As you can see, it gave us a really good result. But one problem we have with workflow one is that it edits the entire image. If you look closely, you'll notice that here the whole image has been edited. In the input image, the subject's face is closer, while in the final output, the subject's face looks a bit farther away. And if you pay attention, the overall image quality has dropped a lot. For example, we've completely lost the skin details that we had in the input image.

00:07:47
This one here, that quality simply doesn't exist anymore in the output image. Why does this happen? Because when you use QN image edit in workflow one, even if you specifically tell it in the prompt, I only want you to put the dress on the subject. While it does put the dress on very well and it looks like it hasn't touched the other areas, in reality, your image has been altered. If you examine carefully, you'll notice that sometimes even the face of the person changes in certain outputs. And

00:08:11
this is exactly where workflow 2 solves that problem for us. If you take a look here in Workflow 2, we can mask the areas that we want to be edited. I've placed workflow 2 here for you. It has both a GGUF version and the original version. You can just drag and drop it into your Conf UI workflow. Now, as you can see in the first input image node, I can simply rightclick and choose open in mask editor. Then I can paint over the areas where I want the edit to happen. Any area I don't paint over will not be

00:08:38
touched by the AI at all. And this is the secret to preserving the quality of the input image. We don't allow the AI to degrade the rest of the photo. Here, let me clear the mask once and show you how to paint it again. But before that, one thing to keep in mind. First, look at your clothing image and visualize in your mind which areas need to be masked. For example, if you look at this dress I have here, the upper chest and neckline are uncovered and the clothing only covers from here downward. So, when I

00:09:02
mask my subject image, I don't need to paint over the upper chest area because the clothing won't cover that part anyway. But if you have a dress like this one here where even the upper part of the chest is covered, then you need to mask those areas as well so that the clothing will be applied properly. Inside the mask editor, I'll paint over the areas I want changed. I'll also make my mask a little larger than needed so the AI has enough room to work with. Then I just click save, hit run, and

00:09:27
that's it. You can see how clean the output is. The parts we didn't want to be edited are completely untouched. And that's just incredible. You can see that the original quality of the photo is fully preserved. And the areas that didn't need editing were not changed at all. Even the subject hasn't been shifted, they remain exactly in place. Only the areas that needed editing were modified. In workflow one, you don't have this masking feature. So, if you want to make sure your photo's original

00:09:56
quality is perfectly preserved, and the parts that don't need editing remain completely unchanged, you must use workflow 2. Let me show you a few more examples. Here's another sample. You can see I masked these areas. This is the before image, and this is the after image. If I show you the clothing image I used here, you can see that the entire outfit has been placed onto the subject perfectly without altering the original design of the clothing at all. The rest of the photo remains completely

00:10:22
untouched. Here's the next example. Look closely at the areas I painted for masking. This is the before and this is the after. You can see that the image quality hasn't changed at all. If you zoom in, you'll notice that every pixel from the input image is preserved. Here's the clothing image I used. You can see how accurately the pants and top were applied onto the subject. It's exactly like the original clothing photo, and the quality is simply outstanding. Now, in this example, I

00:10:49
wanted to test the workflow to see if instead of just clothing, it would also work on other wearable items like necklaces. I masked the area where the subject would need to wear the necklace around the neck and upper chest. This is the input image, and this is the output. You can see how accurately it placed the necklace onto the subject. It preserved all the details of the necklace even though it's a very complex design with multiple elements. Something that's usually very difficult for AI to handle.

00:11:17
But here it flawlessly recreated everything without altering the original image. For example, notice this pendant. It has three golden hearts on it in the input image and the workflow perfectly reproduced the same three golden hearts in the output image. This shows the high precision of the workflow. And if you look closely, the quality of the input photo hasn't changed at all. The subject's face, the skin details, and the hair details remain exactly like the input photo with workflow one. However,

00:11:46
you don't get this same quality and authenticity. Let's run the example using workflow one. Here, I gave it another necklace. And if you look at the output, the entire image has changed. We've lost the skin details compared to the input image. Even though the necklace itself was applied well onto the subject's neck, the skin details were lost. The subject's face has changed slightly, and even the lower parts of the image gain some unwanted artifacts. The face also looks a bit

00:12:12
smaller or shifted, as if it's farther from the camera. Here's another test to see if it can also apply sneakers. Look at this subject. This is the original input image, and you can see how well it put the sneakers onto the subject's feet. One important note for your prompts, you can use terms like image one, image two, or image three to guide the AI and make your instructions clearer. This helps it better understand what you mean. Although if everything is obvious, you don't necessarily need to

00:12:38
use these labels. But to prevent any confusion, it's often helpful. For example, you can write this woman in image one is wearing the necklace from image two. That way, you'll usually get a much more accurate output. And finally, all these images are available in the download link I've provided. You can download them. Promptic images also include the workflow file. If you drag and drop the image into your workflow, all the prompts and the exact settings I used here will be loaded and visible for

00:13:02
you. You can use them as inspiration. Thank you so much for watching the video. That's it for now. Goodbye.

---

## Video 2: Change Background Workflow V2

00:00:00
Imagine this. You drop your product photo into the workflow and in just a few seconds, the entire background transforms into a new scene. Yet, the subject remains 100% untouched. No distortion, no texture loss, no shifted proportions. Even the smallest details like printed text, tiny labels, textures, reflections, and edges stay exactly the same as if nothing ever happened. This is version two of change background and put any subject in any background rebuilt from the ground up to be far more powerful than version one.

00:00:36
Instead of relying on a stable fusion 1.5 or flux which often struggle to preserve authenticity, this new generation is powered by Quin Image Edit Plus optimized with a specific Laura. You choose the background or let the workflow generate one for you and the subject automatically blends into the new scene. Matching lighting and colors with insane accuracy. It's not just background replacement, it's perfect preservation. Let's dive into that. Hey guys, in this video we have a new model,

00:01:09
new workflow for changing background that I name it version two because previously we had change background version one in my YouTube channel with the SE fusion 1.5. But in this one, we have Quan image edit, one of the most powerful models out there for editing images. And in this workflow, you will be amazed. I'm so excited to introduce it to you. Without further ado, let's check the workflow and tell you how you should work with it. Let me show you the quantage edit simple workflow, the main

00:01:40
workflow of quan image edit plus that already by using it you can easily change the background of any image. For example, I have this car with a almost white background and in the prompt this car on a display at an indoor auto show surrounded by spotlight and glossy reflection blah blah blah. And the result is this. Not bad so far. But the problem is when you use the con image edit main workflow which is the simplest one the product image or I should say the subject image is changed a bit. As you can see we have this car a bit

00:02:19
shifted you know and it's not the exact image we had in the input image. This is input image and this is the result. there are a lot of shifts and sometimes in some cases the car is changed and some elements are not correct or if I show you another example this is coin image edit simple workflow and as you can see in this example it is more obvious this bottle of perfume has been changed here the height of the bottle as you can see and the box of it has been changed and in most of cases we don't

00:02:55
want that And many of you had asked me over and over that how we can change the background of product while preserving all tiny details. However, the details of our product are preserved even in the con image edit simple workflow. But we want more precision. And here is the magic happen. With this new workflow and some settings and a new Laura, we can achieve this result. Look at this guys. There's no shift on our product and almost everything has been preserved 100% same as the input image. Also, we have reflections on the

00:03:38
car as you can see here and the lighting and perspective. Everything is perfect. I will show you how to use this workflow. And also check this out. This is the other one. If you remember, I showed you the result generated with quin image main workflow, the product has been changed. But in the new workflow, as you can see, everything is perfect and precise. And I will tell you a way that you can mix these two. This result, because somehow this result is a bit more cinematic and maybe more eye-catching for some of you. Maybe some

00:04:21
of you prefer this one or some of you prefer this. This completely depends on your work and your needs. Maybe someone needs an output between these two. I will tell you everything in the coin image edit workflow. As you can see, we have an input image and a prompt that describe what I want in a background. And the model works very well. But there are some differences between this workflow and this one. The first one is removing background node. We have a remove background node here. And this workflow works better with a product

00:04:59
with a transparent background. So we add this. And this image goes to the new text encode coin image edit plus the advanced one as you can see here. And also we have a new Laura here. In this example, we don't have the second lura. The first lura as you know is coin image lighting adep lura which allows us to use a step instead of 25 step which is the default number of steps for co image edit. But by using this lura we can use a step and make our process very fast. And in this new workflow change

00:05:36
background version two we have the lighting lura plus white to scene lura. All the instructions to download the models, the main quant image model, the text encoder model, also the VAE and these two loras are explained in these notes. These are main models of coin image edit plus and the lighting lura and the main lura for changing background white to scene Laura. This one should be download from this link. And there is an explanation here that I explained to you what is this and what can this workflow and lura do. The

00:06:11
trigger word is this one because this lura has been made by a Chinese guy and I will show you his page in the hugging face. This user DX8152 has made this lura. I should thank him for such amazing work. And the trigger word he set on this lura is this. And the meaning is this white background image to scene conversion. And you need to put the trigger word here in this note. And you must not change it. Leave it as it is here. And for your prompt, you can use Chinese prompt or English prompt. It doesn't matter. But somehow

00:06:49
while you are using this lura, the Chinese prompt should work better. But I'm not 100% sure about that. You can experiment it yourself. In this example, I didn't use any Chinese prompt and I use an English prompt. But the trigger word should be Chinese. Keep this in your mind. Okay. After you download the Laura and put it in this directory, we can use this workflow. It is very simple and straightforward. We can change the seed and test it again in this video. Let me change the seed. I set it in

00:07:26
randomize and run the workflow again. This is coin image edit simple workflow which is the main workflow of coin image edit. And as you can see the result is good. The reflections are very good but the product changes a bit in coin image edit main workflow. Let me copy this seed and paste it here to use a same fixed seed to see the difference. Okay, I run the workflow and this is the result. As you can see, there's no shift and no change in the product and the lighting is perfect. The shadows, the reflections are 100%

00:08:16
perfect for this generation. But what if you want an output between these two results? The more cinematic vibe of this image and the precision of this image. Maybe you can guess it, but if not, I will tell you. In this node for the lura of vittosine you can decrease the value of the lura to make it less effect on your final output. For example I set it on 50 and with the same seat I press run and this is the new result. As you can see, the lights are a bit more cinematic and somehow warmer and I think I like it

00:09:01
more than the previous one. There is no change in the product as well. This is amazing. Fantastic guys. Even the reflections are very accurate. Also, we can check this example too. You see output is amazing. And if I decrease the value of the lura to 50. Let's check how it works. And this is the result. As you can see, we have a little shift here, but not significant. And everything is the same as our input image. While we have the TV reflections on the window here and the light reflections on the hood of the

00:09:49
car, also the front glass of the car has the reflections too. And everything is amazing, guys. We have the cinematic vibe like this one. But without the Laura, you see a lot of shifts had been occurred here. This workflow is very useful for some products that has tiny details or specific textures and you can experiment yourself. In the main video for our YouTube, I will show you more examples of the products that have tiny details or some specific textures. And this workflow is great for those who want

00:10:27
more precision over cinematic or professional lighting. This is fantastic, guys. And also we have another workflow. If you remember we had put any subject any background version one in my channel and you could put any subject in any background but the precision wasn't so good. However, it was very useful and many of you have been using it for a long time but this one trust me is more accurate and more reliable and I like it so much. Let's see what we have here. I started with quin image edit simple workflow and the

00:11:07
main workflow. And for this one, I put some subject on a background manually with Photoshop and ask AI to place these products in the image and blend it together. As you can see in Photoshop, I have this vase and this teapot and they were like this and this and I removed their background and put them in this image on a desk in a kitchen. As you can see, there is no lighting. There is no shadows and everything about lighting and perspective are off. And we want the model, the new put any subject in the

00:11:44
image workflow to blend these images together. We haven't had even a single workflow or model which can handle this task. Many of you have been asking me what workflow can handle this work precisely and beautifully and I didn't have anything with this level of quality and precision and let's see how the model handles it. This is the coin image simple workflow and not the new workflow because as you know the coin image edit very powerful model to edit images and it can handle lighting and and works

00:12:19
like this. Let me show you the translation of this sentence. My prompt is blend the image, correct the products perspective and lighting and integrate the product into the background. Pour in hot tea. Okay, this is the result. This is the result we get from coin image edit main workflow. Not bad but as you can see there are some artifacts and changes in the products. Also the quality of the image is a bit low. And as you can see in the background we have some pixelated issues. And let's test it

00:12:54
with new workflow. Put any subject version two. And look at the result guys. Absolutely amazing. Absolutely amazing. Look at the precision guys. If you notice the vase is 100% unchanged and a little lighting has been added to it because the lighting of the environment is a bit different from the vase and this work should be done by the workflow. It could handle it perfectly and I really like the result about the vase and about the teapot. As you can see the perspective of the teapot is a bit off. You can see the angle of teapot

00:13:34
or the let of teapot is a bit off and the model could change it and it's not the downside of the model. If you see some changes here at the top of the teapot, these changes has been occurred because the perspective of the teapot is not 100% accurate compared to the desk and the perspective of the camera. You know, this is magic, guys. And the quality is absolutely amazing. There's no pixelation here. And as you can see, the reflections are so good. And the edges of the product, as you can see in

00:14:11
the input image, there are so many pixelated edges here. And everything has been fixed. And I really like the result, guys. It's perfect. It's 100% accurate in my opinion. And let's see another example. This is another example. I add this car in this background. As you can see in the Photoshop, I put this car in this background. And you see there are separated layers. This is the main image of the car. And this is the background. I put it here and masked it. As you can see, the perspective is a bit off and

00:14:46
also the lighting. And let's see how this new model can handle this. Look at the precision, guys. Look at the quality. As you can see, back of the car has been fixed. Its perspective wasn't match the background. And as you can see, there's a little shift of its back and the front of the car is amazing, guys. Everything is perfect. The reflections, the shadows underneath the car, the lightings, the orange lights here, and everything is perfect. And if you want to see the output of the coin

00:15:24
image edit main workflow without the lura, you see this is the result. We have quality loss, some changes to the car that I think is not perfect. The result is not bad, but but we want more accurate results when it comes to lighting products and match it with our specific background. This is a very hard work for AI to do. This is so hard. But with the help of this Lura, as you can see, the result is so much accurate and eye-catching. I forgot about the second Lura. This Laura is different from the change background Lura. As you can

00:16:05
see, the Laura name is white to scene in this example in the change background workflow. But in this workflow, we have Fusion Laura. You can download it from this link. As you can see here, the same guy and the Fusion Laura. You should download this model and you can rename it to find it easier. I've changed it name and I named it Fusion Laura. And as the previous one, you can play with the value of the Laura. And the main difference between this workflow put any subject and change background as you

00:16:46
know is that in this workflow change background you will create the background through a prompt. Okay, we don't have any background here. We just give it an input image with a white background. I forgot about this important note. You should use a white background for your product or as simple as this image. So don't forget to use a product with a white background or a simple background. The main difference between this workflow and this one is that in the change background workflow, you don't have any background and it

00:17:26
will create the background for you through a prompt. But in this workflow, we have the background and we have our product images. But we put the background and the products using Photoshop or any software you want. You can add more products as many as you want. 1 2 3 or four. It can handle it perfectly. We put our products in the background and save it. It will blend these two images together perfectly. Because many of you has been asking me that we have our specific background and we don't want that AI generate the

00:18:05
background for us through a prompt. We want to use our specific background and this workflow is for you and for those who want to create background through a prompt and they don't have any pre-made background or pre-generated background they can use this workflow. Both are really powerful and useful. I hope you enjoy the video. You can download the workflows in the W or Booy. Thank you. I see you in next videos.
