
# TODO

Analyze the existing @core and @engines code. 

Then create a new engine `fal` that takes our parsed core `MidjargonDict` and converts it into a very LIGHTWEIGHT Pydantic model for Fal. The moden would then be serialized into a JSON object that can be sent to the Fal.ai API.

Below are some examples of the JSON payloads for the various Fal.ai models. Of notable differences, the `aspect` entry from the `MidjargonDict` needs to be converted to what's ultimately `aspect_ratio` in the Fal.ai API.

Also, as a special treatment, we should build the `"image_url"` entry so that we first check if there's explicitly "image_url" supplied in the `MidjargonDict`, and we use it if there is but if not, we try to take the 1st out of the `image_prompts` and use it as the `image_url`.

First make a detailed plan for the `fal` engine. Then implement it. I don’t think there is any need at this point to modify the EXISTING code! 


### Fal.ai Ideogram

https://fal.ai/models/fal-ai/ideogram/v2?share=514b914e-05f0-4e83-b09a-1a51430083be

```json
{
  "style": "auto",
  "prompt": "A marble-skinned figure with neoclassical features, matte skin, and wrinkles, majestically strides forward on a serene tropical beach with a palm tree and green foliage, amidst a blurred bustling galactic trade hub background.",
  "aspect_ratio": "1:1",
  "expand_prompt": true
}
```

### Fal.ai Recraft

https://fal.ai/models/fal-ai/recraft-v3?share=cbcfda7e-72d5-4a5d-bf4c-c0e699a7ac7a

```json
{
  "style": "realistic_image",
  "colors": [],
  "prompt": "A mesmerizing nighttime scene of a fantastical urban landscape, featuring an intricately designed building illuminated by vibrant neon lights. The architecture boasts ornate windows and patterns in a variety of colors such as pink, blue, orange, and green, creating a surreal and captivating atmosphere. The surrounding streets are empty, providing a contrast between the bustling building and the quiet surroundings. The 3D render has a cinematic quality, with elements of anime and dark fantasy, evoking a sense of wonder and mystery. The overall composition is a masterful blend of architecture, style, and conceptual art reminiscent of ukiyo-e., 3d render, photo, cinematic, architecture, anime, dark fantasy, illustration, ukiyo-e, conceptual art, vibrant",
  "image_size": "landscape_4_3"
}
```

### Fal.ai Auraflow

https://fal.ai/models/fal-ai/aura-flow?share=99d2cb8c-8393-4d58-b26c-dfbed2818c71

```json
{
  "seed": 2883281709,
  "prompt": "A refreshing scene where a glass of freshly squeezed orange juice stands prominently at the center, bathed in warm, golden sunlight that highlights the vibrant, citrus hues of the juice. The glass is intricately detailed, showing condensation droplets that glisten like tiny jewels. Surrounding the base of the glass, scattered orange slices and lush green leaves add a touch of natural beauty and freshness. Above the glass, a dynamic splash of orange juice is captured mid-air, forming the word \"Orange\" in a fluid, playful script. The splash is so vivid and realistic that each droplet seems to dance in the air, creating a sense of movement and energy. In the background, a serene orchard with rows of orange trees stretches out under a clear blue sky, their branches heavy with ripe oranges ready for harvest. Rays of sunlight filter through the leaves, casting dappled shadows on the ground. A gentle breeze rustles the leaves, adding a sense of calm and tranquility to the scene. The entire scene evokes a sense of purity, freshness, and vitality, inviting viewers to experience the simple joy of a glass of fresh orange juice.",
  "num_images": 1,
  "guidance_scale": 3.5,
  "num_inference_steps": 50
}
```

### Fal.ai Flux dev

https://fal.ai/models/fal-ai/flux/dev?share=ec3713ef-099d-4700-8939-286a4d6f5756

```json
{
  "seed": 2167289645,
  "prompt": "portrait | wide angle shot of eyes off to one side of frame, lucid dream-like woman, looking off in distance,style | daydreampunk with glowing skin and eyes, styled in headdress, beautiful, she is dripping in neon lights, very colorful blue, green, purple, bioluminescent, glowing background | forest, vivid neon wonderland, particles, blue, green, purple, parameters | rule of thirds, golden ratio, assymetric composition, hyper- maximalist, octane render, photorealism, cinematic realism, unreal engine, 8k",
  "image_size": "landscape_4_3",
  "num_images": 1,
  "guidance_scale": 3,
  "num_inference_steps": 28,
  "enable_safety_checker": true
}
```

### Fal.ai Flux Lora

https://fal.ai/models/fal-ai/flux-lora?share=0363ac29-8a48-4218-8837-3b142b063224

```json
{
  "loras": [
    {
      "path": "https://huggingface.co/multimodalart/flux-tarot-v1/resolve/main/flux_tarot_v1_lora.safetensors"
    }
  ],
  "prompt": "a trtcrd of a person on a computer, on the computer you see a meme being made with an ancient looking trollface, \"the shitposter\" arcana, in the style of TOK a trtcrd, tarot style",
  "image_size": "landscape_4_3",
  "num_images": 1,
  "output_format": "jpeg",
  "guidance_scale": 3.5,
  "num_inference_steps": 28,
  "enable_safety_checker": true
}
```

### Fal.ai Flux Subject

https://fal.ai/models/fal-ai/flux-subject?share=2a99ed04-9675-4dcb-888f-41099df90239

```json
{
  "prompt": "logo on a hat",
  "image_url": "https://v3.fal.media/files/koala/pzQe4LVpsFRilCuh0JhsK_smaller.png",
  "num_images": 4,
  "output_format": "png",
  "guidance_scale": 3.5,
  "num_inference_steps": 4,
  "enable_safety_checker": true
}
```

