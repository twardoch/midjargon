# **Midjourney Prompt Format Specification**

A Midjourney prompt uses the "midjargon": a structured text syntax that instructs the Midjourney Bot to generate images. The prompt consists of three main sections, in order:

1. **Image Prompts (Optional)**
2. **Text Description (Required if no image is provided)**
3. **Parameters (Optional)**

Each section has a defined syntax and placement requirement. Advanced features (such as multi-prompts with weights and permutation prompts) are integrated into the text description and parameters.

---

## [∞](#1-image-prompts) **1. Image Prompts**

- **Definition:**  
  One or more direct image URLs used to influence the generated image's style, color, and composition.
  
- **Syntax & Placement:**  
  - Must appear at the very start of the prompt.
  - Each URL must be a direct link ending with one of the following extensions:  
    `.png`, `.jpg`, `.jpeg`, `.gif`, or `.webp`.
  - Multiple image URLs are separated by whitespace.  
  - *Example:*  
    ```
    https://example.com/image1.jpg https://example.com/image2.png
    ```

- **Optional Adjustments:**  
  - **Image Weight (`--iw`)**:  
    Adjusts the influence of image prompts relative to the text prompt.
    - **Syntax:** `--iw <value>`
    - **Value Range:** 0.0 to 3.0 (float)
    - **Default:** 1.0
    - *Example:*  
      ```
      --iw 1.5
      ```
  - **Style Reference (`--sref`)**:
    Uses images as style references without influencing content.
    - **Syntax:** `--sref <url1> [url2...]`
    - **Value:** One or more image URLs
    - *Example:*  
      ```
      --sref https://example.com/style.jpg
      ```

---

## [∞](#2-text-description) **2. Text Description**

- **Definition:**  
  A natural language description of the desired image. This is the core creative input where you specify the subject, mood, style, and other artistic details.

- **Guidelines:**
  - **Clarity & Specificity:**  
    Use specific adjectives, nouns, and phrases. Describe the subject, medium (e.g., photo, painting), environment, lighting, color, mood, and composition.
  - **Positive Framing:**  
    Emphasize what should appear in the image rather than what should be excluded (exclusions are handled by the `--no` parameter).
  - **Tokenization:**  
    The text is tokenized internally; word order and precision are important.

- **Advanced Constructs:**
  - **Multi-Prompts & Weights:**  
    Separate distinct concepts using a double colon (`::`), optionally followed by a weight.
    - **Syntax:**  
      ```
      concept1 ::<weight1> concept2 ::<weight2> ...
      ```
      If a weight is omitted, a default of 1 is assumed.
    - **Weight Range:** -10.0 to 10.0 (float)
    - **Negative Weights:**  
      Use negative numbers (e.g., `::-.5`) to de-emphasize or effectively exclude a concept.
    - *Examples:*  
      ```
      futuristic city ::2 cyberpunk skyline ::1
      beautiful landscape ::1.5 mountains ::-0.5 water
      ```
  
  - **Permutation Prompts:**  
    Create multiple prompt variations by including comma-separated options within curly braces `{}`.
    - **Syntax:**  
      ```
      Some fixed text {option1, option2, option3} more fixed text
      ```
    - **Rules:**
      - All options are combined with the surrounding text to generate separate variations.
      - **Nesting:**  
        Nested curly braces are allowed for more complex combinations.
      - **Escaping:**  
        To include a literal comma within an option, escape it with a backslash (`\,`).
      - **Parameter Permutations:**  
        Permutations can include parameters and their values.
    - *Examples:*  
      ```
      # Basic permutation
      A {red, blue, green} bird on a {flower, leaf}

      # With escaped comma
      A {solid\, bright, pale\, soft} color

      # With parameters
      A portrait {--ar 1:1, --ar 16:9} {--stylize 100, --stylize 1000}
      ```

---

## [∞](#3-parameters) **3. Parameters**

Parameters are modifiers appended at the end of the prompt that adjust various aspects of image generation. They always begin with two hyphens (`--`) and may accept a value. The order of parameters (after the text description) is generally flexible.

### [∞](#31-composition-and-formatting-parameters) **3.1. Composition and Formatting Parameters**

- **Aspect Ratio:**  
  - **Purpose:** Sets the width-to-height ratio of the image.
  - **Syntax:**  
    ```
    --ar <width>:<height>
    ```
    (An alternate flag is `--aspect`.)
  - **Value Format:** Two integers separated by a colon
  - **Common Ratios:** `1:1`, `16:9`, `4:3`, `3:2`
  - **Example:**  
    ```
    --ar 16:9
    ```
  - **Notes:**  
    Both `<width>` and `<height>` must be whole numbers. Default is 1:1.

- **Tile:**  
  - **Purpose:** Creates images that are seamlessly tileable.
  - **Syntax:**  
    ```
    --tile
    ```
  - **Value:** None (boolean flag)
  - **Example:**  
    ```
    --tile
    ```

- **Repeat:**  
  - **Purpose:** Runs the same prompt multiple times to generate variations.
  - **Syntax:**  
    ```
    --repeat <number>
    ```
    (Also available as `--r <number>`.)
  - **Value Range:** 
    - Basic Subscribers: 2–4  
    - Standard Subscribers: 2–10  
    - Pro/Mega Subscribers: 2–40
  - **Example:**  
    ```
    --repeat 5
    ```

### [∞](#32-randomness-and-variation) **3.2. Randomness and Variation**

- **Chaos:**  
  - **Purpose:** Controls the degree of variation or unpredictability in the generated output.
  - **Syntax:**  
    ```
    --chaos <value>
    ```
    (Also available as `--c <value>`.)
  - **Value Range:** 0 to 100 (integer)
  - **Default:** 0
  - **Example:**  
    ```
    --chaos 50
    ```

- **Seed:**  
  - **Purpose:** Sets the random seed to reproduce specific outcomes.
  - **Syntax:**  
    ```
    --seed <value>
    ```
  - **Value Range:** 0 to 4294967295 (integer)
  - **Example:**  
    ```
    --seed 123456789
    ```

### [∞](#33-style-and-aesthetic-control) **3.3. Style and Aesthetic Control**

- **Stylize:**  
  - **Purpose:** Adjusts how strongly Midjourney's default artistic style is applied.
  - **Syntax:**  
    ```
    --stylize <value>
    ```
    (Alternate flag: `--s <value>`.)
  - **Value Range:** 0 to 1000 (integer)
  - **Default:** 100
  - **Example:**  
    ```
    --stylize 250
    ```

- **Weird:**  
  - **Purpose:** Introduces unconventional or experimental visual elements.
  - **Syntax:**  
    ```
    --weird <value>
    ```
    (Alternate flag: `--w <value>`.)
  - **Value Range:** 0 to 3000 (integer)
  - **Default:** 0
  - **Example:**  
    ```
    --weird 1000
    ```

- **Style:**  
  - **Purpose:** Applies a specific aesthetic preset or a raw mode.
  - **Syntax:**  
    ```
    --style <style_name>
    ```
  - **Common Values:**  
    - `raw`: Reduces automatic stylization
    - `expressive`: Enhances artistic interpretation
    - `cute`: Applies a cute, cartoon-like style
  - **Example:**  
    ```
    --style raw
    ```

### [∞](#34-model-and-iteration-control) **3.4. Model and Iteration Control**

- **Version:**  
  - **Purpose:** Selects which Midjourney model version to use.
  - **Syntax:**  
    ```
    --v <version_number>
    ```
  - **Common Values:**  
    - `5`, `5.1`, `5.2`: Version 5 series
    - `6`: Latest version 6
  - **Niji Model:**  
    Use `--niji <version_number>` for the Niji model (optimized for anime/illustration).
  - **Examples:**  
    ```
    --v 5.2
    --niji 6
    ```

- **Stop:**  
  - **Purpose:** Stops the image generation process at a specified percentage of completion.
  - **Syntax:**  
    ```
    --stop <value>
    ```
  - **Value Range:** 10 to 100 (integer)
  - **Default:** 100
  - **Example:**  
    ```
    --stop 80
    ```

### [∞](#35-exclusion-parameters) **3.5. Exclusion Parameters**

- **No:**  
  - **Purpose:** Explicitly excludes specified elements from the image.
  - **Syntax:**  
    ```
    --no <item1, item2, ...>
    ```
  - **Value Format:** Comma-separated list of terms
  - **Example:**  
    ```
    --no cars, trees, watermarks
    ```
  - **Note:** This acts similarly to applying a negative weight to concepts in multi-prompts.

---

## [∞](#4-advanced-prompting-features) **4. Advanced Prompting Features**

### [∞](#41-multi-prompts-with-weighting) **4.1. Multi-Prompts with Weighting**

- **Purpose:**  
  To blend or balance multiple distinct concepts within one prompt.
- **Syntax:**  
  ```
  concept1 ::<weight1> concept2 ::<weight2> concept3 ...
  ```
  - **Weights:**  
    - When omitted, a default weight of 1 is assumed.
    - Negative weights (e.g., `::-0.5`) reduce the prominence of a concept.
    - Weight values can be floating-point numbers.
- **Examples:**  
  ```
  # Basic weighting
  serene lake ::2 foggy mountains ::1

  # With negative weights
  beautiful landscape ::1 urban elements ::-0.5

  # Complex mixing
  portrait ::1.5 dramatic lighting ::1 dark background ::0.8
  ```

### [∞](#42-permutation-prompts) **4.2. Permutation Prompts**

- **Purpose:**  
  Quickly generate multiple variations of a prompt by providing several options for parts of the text.
- **Syntax:**  
  - Enclose a comma-separated list of options within curly braces `{}`.
  - The surrounding fixed text is combined with each option to produce different variations.
  - **Basic Example:**  
    ```
    A {red, blue, green} car
    ```
    Expands to:  
    - "A red car"  
    - "A blue car"  
    - "A green car"
- **Advanced Features:**
  - **Nested Permutations:**  
    ```
    A {red, blue} {car, truck} with {chrome, matte} finish
    ```
  - **Parameter Permutations:**  
    ```
    portrait --ar {1:1, 16:9} --stylize {100, 500, 1000}
    ```
  - **Mixed Content:**  
    ```
    {realistic, artistic} scene {--v 5, --v 6} {--style raw, }
    ```
  - **Escaping:**  
    ```
    A {bright\, vibrant, dark\, moody} atmosphere
    ```

---

## [∞](#5-complete-prompt-structure-examples) **5. Complete Prompt Structure Examples**

1. **Basic Text-Only Prompt:**  
   ```
   /imagine prompt: A serene sunset over the ocean
   ```

2. **Prompt with Image URL, Text, and Parameters:**  
   ```
   /imagine prompt: https://example.com/inspiration.jpg A portrait of a wise old man --style raw --v 5.1
   ```

3. **Multi-Prompt with Weighting:**  
   ```
   /imagine prompt: futuristic city ::2 cyberpunk skyline ::1 --chaos 20
   ```

4. **Permutation Prompt for Multiple Variations:**  
   ```
   /imagine prompt: A {red, blue, green} bird on a {flower, leaf} --ar 16:9
   ```

5. **Complex Mixed Prompt:**  
   ```
   /imagine prompt: https://example.com/ref.jpg 
   {realistic, artistic} portrait of a {young, old} {man, woman} 
   --style {raw, expressive} --v 6 --ar 1:1 --stylize {100, 1000}
   ```

6. **Prompt with Multiple Parameters:**  
   ```
   /imagine prompt: A futuristic landscape at dusk 
   --ar 21:9 --stylize 300 --chaos 50 
   --seed 987654321 --no buildings,cars
   ```

---

## [∞](#implementation-notes) **Implementation Notes**

### Parsing Order

1. **Image URL Extraction:**
   - Identify and validate URLs at the start of the prompt
   - Check for supported file extensions
   - Handle multiple URLs

2. **Permutation Expansion:**
   - Process all permutation groups `{...}`
   - Handle nested permutations
   - Expand into individual prompts

3. **Parameter Processing:**
   - Extract parameters starting with `--`
   - Parse parameter values
   - Handle boolean flags
   - Validate parameter ranges

4. **Text Processing:**
   - Extract main prompt text
   - Process weight markers `::`
   - Handle escaped characters

### Parameter Handling

- **Boolean Parameters:**
  If a parameter is followed by another parameter (e.g., `--tile --ar 16:9`), it's treated as a boolean flag.

- **Multi-Value Parameters:**
  Some parameters can accept multiple values (e.g., `--no cars,trees`). These are typically comma-separated.

- **Parameter Validation:**
  - Numeric ranges are enforced
  - Aspect ratios must be valid integers
  - Version numbers must be supported
  - Style names must be recognized

### Error Handling

The parser should handle common errors gracefully:

- Invalid URL formats
- Malformed permutation syntax
- Invalid parameter values
- Missing required components
- Unsupported parameter combinations

---

## [∞](#summary) **Summary**

- **Order Matters:**  
  Image URLs come first (if used), followed by the text description, and then all parameters.

- **Parameter Prefix:**  
  Every parameter starts with `--` and (if required) is followed by a space and its value.

- **Advanced Techniques:**  
  Use multi-prompts with `::` and permutation prompts with `{}` to fine-tune creative direction and generate multiple variations.

- **Model and Feature Dependencies:**  
  Some parameters (e.g., `--iw`, `--stop`, `--v`/`--niji`, permutation prompts) are model-specific or depend on the subscription tier or mode (e.g., Fast mode).

## Notes

When parsing midjargon, we need to first permute (expand the {} into simple prompts), then parse each of the simple prompts.

### Null values

If a --param2 directly follows another --param1, then --param1 is present but has a null value (equivalent to a boolean True). But nonparams that follow a --param1 become its values, and can be multiple

### Permutation prompts

This prompt: 

```input
a {black, white, red\,blue} cat {, --p {, PERSOCODE}} --ar {16:9}
```

should permute into 9 prompts:

```permutation
a black cat --ar 16:9
a black cat --p --ar 16:9
a black cat --p PERSOCODE --ar 16:9
a white cat --ar 16:9
a white cat --p --ar 16:9
a white cat --p PERSOCODE --ar 16:9
a red,blue cat --ar 16:9
a red,blue cat --p --ar 16:9
a red,blue cat --p PERSOCODE --ar 16:9
```
---

```input
{bulldog, dachshund} cute claymation character --no blur --style raw --ar {16:9, 1:1} {--p m7284532597038776332, --p} --s {150, 800}
```

```permutation
bulldog cute claymation character --no blur --style raw --ar 16:9 --p m7284532597038776332 --s 150 --ar 16:9
bulldog cute claymation character --no blur --style raw --ar 16:9 --p m7284532597038776332 --s 800 --ar 16:9
bulldog cute claymation character --no blur --style raw --ar 16:9 --p --s 150 --ar 16:9
bulldog cute claymation character --no blur --style raw --ar 16:9 --p --s 800 --ar 16:9
bulldog cute claymation character --no blur --style raw --ar 1:1 --p m7284532597038776332 --s 150 --ar 16:9
bulldog cute claymation character --no blur --style raw --ar 1:1 --p m7284532597038776332 --s 800 --ar 16:9
bulldog cute claymation character --no blur --style raw --ar 1:1 --p --s 150 --ar 16:9
bulldog cute claymation character --no blur --style raw --ar 1:1 --p --s 800 --ar 16:9
dachshund cute claymation character --no blur --style raw --ar 16:9 --p m7284532597038776332 --s 150 --ar 16:9
dachshund cute claymation character --no blur --style raw --ar 16:9 --p m7284532597038776332 --s 800 --ar 16:9
dachshund cute claymation character --no blur --style raw --ar 16:9 --p --s 150 --ar 16:9
dachshund cute claymation character --no blur --style raw --ar 16:9 --p --s 800 --ar 16:9
dachshund cute claymation character --no blur --style raw --ar 1:1 --p m7284532597038776332 --s 150 --ar 16:9
dachshund cute claymation character --no blur --style raw --ar 1:1 --p m7284532597038776332 --s 800 --ar 16:9
dachshund cute claymation character --no blur --style raw --ar 1:1 --p --s 150 --ar 16:9
dachshund cute claymation character --no blur --style raw --ar 1:1 --p --s 800 --ar 16:9
```

---

```input
comic strip in style of {John, Bill}, bright colors --s {20, 999} --sref https://picsum.photos/id/237/200/300 https://picsum.photos/200/300?grayscale --sw {20, 999}
```

```permutation
comic strip in style of John, bright colors --s 20 --sref https://picsum.photos/id/237/200/300 https://picsum.photos/200/300?grayscale --sw 20 --ar 16:9
comic strip in style of John, bright colors --s 20 --sref https://picsum.photos/id/237/200/300 https://picsum.photos/200/300?grayscale --sw 999 --ar 16:9
comic strip in style of John, bright colors --s 999 --sref https://picsum.photos/id/237/200/300 https://picsum.photos/200/300?grayscale --sw 20 --ar 16:9
comic strip in style of John, bright colors --s 999 --sref https://picsum.photos/id/237/200/300 https://picsum.photos/200/300?grayscale --sw 999 --ar 16:9
comic strip in style of Bill, bright colors --s 20 --sref https://picsum.photos/id/237/200/300 https://picsum.photos/200/300?grayscale --sw 20 --ar 16:9
comic strip in style of Bill, bright colors --s 20 --sref https://picsum.photos/id/237/200/300 https://picsum.photos/200/300?grayscale --sw 999 --ar 16:9
comic strip in style of Bill, bright colors --s 999 --sref https://picsum.photos/id/237/200/300 https://picsum.photos/200/300?grayscale --sw 20 --ar 16:9
comic strip in style of Bill, bright colors --s 999 --sref https://picsum.photos/id/237/200/300 https://picsum.photos/200/300?grayscale --sw 999 --ar 16:9
```
---

