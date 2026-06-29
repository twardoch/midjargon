# Midjourney Prompt Format Specification

_2025-02-06 by Adam Twardoch, not affiliated with Midjourney_

Midjourney prompts use structured syntax to generate images. A prompt contains three sections in order:

1. **Image Reference** (optional)
2. **Text Description** (required if no image provided)
3. **Parameters** (optional)

Each section has specific syntax requirements. Advanced features like multi-prompts, permutations, personalization, and style references are part of the text description or parameters.

Midjourney supports two types of stylization that are often confused in documentation:

- Style reference
- Personalization

## Parameters

Parameters modify image generation and appear at the end of the prompt. They start with two hyphens `--` and may take values. Parameter order is flexible.

Terms following a parameter are treated as arguments. If a parameter is immediately followed by another parameter, it acts as a boolean flag.

---

## Model Selection

### Midjourney series (`--v` or `--version`)

Specifies the general Midjourney model version.

#### Syntax

```
--v <version_number>
```

#### Values

- `5`, `5.1`, `5.2`, `6`, `6.1`

> Example

```
--v 6
```

### Niji series (`--niji`)

Uses Niji models optimized for anime and illustration styles.

#### Syntax

```
--niji <version_number>
```

#### Values

- `5`, `6`

> Example

```
--niji 6
```

### Model mode (`--style`)

Applies specific model behavior.

```
--style <mode_name>
```

#### Values

- `raw` (reduces automatic personalization)

> Example

```
--style raw
```

## Image Usage

### Image references

One or more images that influence style, color, composition, and content.

Must appear at the **start** of the prompt.

Each image can be:

- A direct URL ending in `.png`, `.jpg`, `.jpeg`, `.gif`, or `.webp`
- An attached image in Discord or uploaded via web interface

Multiple images separated by whitespace.

> Example

```
https://example.com/image1.jpg https://example.com/image2.png
```

#### Image weight (`--iw`)

Controls influence of all image references relative to text.

`--iw <value>`

- Range: `0.0` to `3.0` (float)
- Default: `1.0` (varies by model)

> Example

```
--iw 1.5
```

Place `--iw` after text description, despite referencing images at prompt start.

### Character reference (`--cref`)

`--cref <url1> [<url2> ...]`

Maintains character consistency across generations.

#### Character weight (`--cw`)

Controls strength of character reference.

`--cw <value>`

- Range: `0` to `100` (integer)
- Default: `100`

Weight `0` typically copies only the face.

> Example

```
--cref https://example.com/character.jpg --cw 50
```

### Style reference (`--sref`)

`--sref <url|code> [<url|code> ...]`

Applies visual characteristics without affecting content. Accepts image URLs or stylization codes.

#### Style weight (`--sw`)

Controls strength of style reference.

`--sw <value>`

- Range: `0` to `1000` (integer)

#### Style version (`--sv`)

Selects style reference algorithms.

`--sv <value>`

- Values: `1`, `2`, `3`, `4`

> Example

```
--sref https://example.com/style.jpg --sw 200 --sv 2
```

#### Random style reference

`--sref random`

Generates random style reference.

### Persona reference (`--p`)

References personalized style profiles or moodboards.

- Without code: uses your current personalization profile
- With code (e.g., `--p p123456789`): applies specific personalization

#### Personalization weight (`--s`)

```
--stylize <value>
```

Controls degree of personalization influence:

- With persona code: pulls toward that persona
- With `--p` but no code: pulls toward your profile
- Without `--p`: pulls toward model's general aesthetic

- Range: `0` to `1000` (integer)
- Default: `100`

Value `0` minimizes personalization. Use `--style raw` with low `--s` for purer personalization.

> Example:

```
--p p123456789 --s 500 --style raw
```

## Text Description

Natural language description specifying subject, mood, style, and artistic details.

### Clarity & specificity

Use specific terms. Describe subject, medium, environment, lighting, color, mood, and composition.

### Positive framing

Specify desired elements. Use `--no` for exclusions.

### Tokenization

Internal tokenization makes word order and precision important.

### Text generation

Use double quotes `"` around text to appear in image.

> Example

```
A neon sign that says "Open"
```

### Negative description (`--no`)

Excludes elements from generation.

```
--no <item1, item2, ...>
```

- Value: comma-separated list

> Example:

```
--no cars, trees, watermarks
```

## Image Layout

### Aspect ratio (`--ar`)

Sets width-to-height ratio.

```
--ar <width>:<height>
```

- Value: two integers separated by colon
- Default: `1:1`

> Example:

```
--ar 16:9
```

### Tile (`--tile`)

Creates seamlessly tileable images.

```
--tile
```

- Boolean flag

> Example:

```
--tile
```

---

## Concept Weighting

Use double colon `::` to separate concepts with optional weights. Default weight is 1.

```
concept1 ::<weight1> concept2 ::<weight2> ...
```

- Weights: `-10.0` to `10.0` (float)
- Negative weights de-emphasize or exclude concepts

### Purpose

Balances multiple concepts in one prompt. Weights maintain proportional relationships internally.

### Examples

```
futuristic city ::2 cyberpunk skyline ::1
beautiful landscape ::1.5 mountains ::-0.5 water
serene lake ::2 foggy mountains ::1
portrait ::1.5 dramatic lighting ::1 dark background ::0.8
still life painting ::1 fruit ::-0.5
```

---

## Variation Controls

### Chaos (`--chaos` or `--c`)

Controls output unpredictability.

```
--chaos <value>
```

- Range: `0` to `100` (integer)
- Default: `0`

> Example

```
--chaos 50
```

### Weird (`--weird` or `--w`)

Introduces unconventional aesthetics.

```
--weird <value>
```

- Range: `0` to `3000` (integer)
- Default: `0`

> Example

```
--weird 1000
```

---

## Generation Process

### Seed (`--seed`)

Reproduces specific outputs.

```
--seed <value>
```

- Range: `0` to `4294967295` (integer)

> Example:

```
--seed 123456789
```

### Prompt permutation

Generates multiple prompts using comma-separated options in curly braces `{}`.

```
A {red, blue, green} car
```

Creates 3 prompts:

- `A red car`
- `A blue car`
- `A green car`

Multiple permutation groups multiply variations:

```
A {red, blue} {car, truck} with {chrome, matte} finish
```

Creates 2×2×2=8 prompts.

Parameters can be permuted:

```
portrait --ar {1:1, 16:9} --s {100, 500, 1000}
```

Creates 2×3=6 prompts.

Nested permutations:

```
{realistic, artistic} scene --v {5.2, 6 {, --style raw}} 
```

Creates 2×(2+1)=6 prompts:

- `realistic scene --v 5.2`
- `realistic scene --v 6`
- `realistic scene --v 6 --style raw`
- `artistic scene --v 5.2`
- `artistic scene --v 6`
- `artistic scene --v 6 --style raw`

Escape commas within groups:

```
A {bright\, vibrant, dark\, moody} atmosphere
```

Creates 2 prompts:

- `A bright, vibrant atmosphere`
- `A dark, moody atmosphere`

Total permutations may be limited by subscription tier. Only available in Fast Mode.

Useful for syntax exploration:

```
beautiful woman{::, ::2, ::0.3, \,} sports car
```

Creates:

- `beautiful woman:: sports car`
- `beautiful woman::2 sports car`
- `beautiful woman::0.3 sports car`
- `beautiful woman, sports car`

### Repeat (`--repeat` or `--r`)

Generates multiple variations on model side. Can combine with permutations.

With `--r`, model runs same prompt multiple times. Use with `--sref random` for different style references each time.

```
--repeat <number>
```

- Range: Basic: 2–4, Standard: 2–10, Pro/Mega: 2–40

> Example:

```
--repeat 5
```

## Quality and Speed

### Quality (`--quality` or `--q`)

Controls generation time and detail level.

```
--quality <value>
```

- Values: `0.25`, `0.5`, `1` (default)

> Example

```
--quality 0.5
```

#### Turbo Mode (`--turbo`)

Faster generation using additional GPU resources.

```
--turbo
```

- Boolean flag

#### Relax Mode (`--relax`)

Generation without consuming GPU time.

```
--relax
```

- Boolean flag

### Stop (`--stop`)

Stops generation at specified completion percentage.

```
--stop <value>
```

- Range: `10` to `100` (integer)
- Default: `100`

> Example:

```
--stop 80
```

---

## Summary

- **Order matters**: Images first, text description second, parameters last
- **Parameter format**: Each starts with `--`, followed by space and value when needed
- **Advanced techniques**: Use `::` for concept weighting, `{}` for permutations
- **Stylization controls**: `--sw` for style reference weight, `--s` for personalization weight
- **Independent effects**: Style references and personalization pull in different directions
- **Testing pure style**: Use `--style raw --s 0`
- **Dependencies**: Some parameters depend on model version, subscription tier, or generation mode
- **Text in images**: Use double quotes `"` for exact text placement

## Prompt examples

1. **Basic text-only:**

```
/imagine prompt: A serene sunset over the ocean
```

2. **With image URLs and parameters:**

```
/imagine prompt: https://example.com/inspiration.jpg A portrait of a wise old man --style raw --v 5.1
```

3. **Character and style references:**

```
/imagine prompt: A hero in battle --cref https://example.com/hero.png --cw 75 --sref https://example.com/style.jpg --sw 150
```

4. **Weighted concepts:**

```
/imagine prompt: futuristic city ::2 cyberpunk skyline ::1 --chaos 20
```

5. **Permutations:**

```
/imagine prompt: A {red, blue, green} bird on a {flower, leaf} --ar {16:9, 1:1}
```

6. **Personalization:**

```
/imagine prompt: A vibrant garden in spring --p p123456789 --stylize 500 --seed 987654321
```

7. **Complex mixed prompt:**

```
/imagine prompt: {realistic, artistic} portrait of a {young, old} {man, woman} --style {raw, expressive} --v 6 --ar 1:1 --stylize {100, 1000}
```

8. **Exclusions and turbo:**

```
/imagine prompt: A futuristic landscape at dusk --ar 21:9 --stylize 300 --chaos 50 --seed 987654321 --no buildings, cars --turbo
```

---

## Notes for parser implementers

### Parsing order

1. **Permutation expansion:**

- Process all `{...}` groups
- Handle nested permutations
- Expand into individual prompts
- `a{b, c}d` → `abd` `acd`
- Collapse spaces around separating commas
- `\{` `\}` `\,` produce literal characters

2. **Image reference parsing:**

- Identify URLs or attachments at start
- Validate file formats
- Handle multiple images

3. **Text description extraction:**

- Extract main prompt text
- Segment by `::` weight markers
- Handle escaped characters
- Identify quoted text for image placement

4. **Parameter processing:**

- Extract `--` prefixed parameters
- Parse values (strings unless obviously numeric)
- Handle boolean flags
- Validate ranges and formats
- Keep version numbers as strings

### Boolean parameters

Parameters followed immediately by another parameter act as boolean flags.

### Multi-value parameters

Some accept comma-separated values (e.g., `--no cars, trees`).

### Validation

- Enforce numeric ranges
- Validate aspect ratios
- Check version support
- Verify style names and codes

### Error handling

Handle gracefully:

- Invalid URLs
- Malformed permutation syntax
- Invalid parameter values
- Missing required components
- Unsupported parameter combinations