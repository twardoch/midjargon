# PROBLEM 1

> python -m midjargon "a {black, white, red, blue} cat {, --p {, PERSOCODE}} --ar 16:9 --style raw --s 200"

│"text": "a blue cat",│
│"image_prompts": [],│
│"stylize": 200,│
│"chaos": null,│
│"weird": null,│
│"image_weight": null,│
│"seed": null,│
│"stop": null,│
│"aspect_width": 16,│
│"aspect_height": 9,│
│"style": "raw",│
│"version": null,│
│"personalization": null,│
│"quality": null,│
│"character_reference": [],│
│"character_weight": null,│
│"style_reference": [],│
│"style_weight": null,│
│"style_version": null,│
│"repeat": null,│
│"turbo": false,│
│"relax": false,│
│"tile": false,│
│"negative_prompt": null,│
│"extra_params": {│
│"personalization": "PERSOCODE"│
│}

So there is `"personalization": null,` AND `"extra_params": {"personalization": "PERSOCODE"}`

# PROBLEM 2

> python -m midjargon "a {black, white, red, blue} cat {, --p {, PERSOCODE}} --ar 16:9 --style raw --s 200 --sw 300"

Error: Invalid parameter name: style_weight

# PROBLEM 3

> python -m midjargon "a {black, blue} cat --ar 16:9 --style raw --s 200" --raw

╭─────────────────────────────────────────────────────────────────────────── Raw Prompt 1 ───────────────────────────────────────────────────────────────────────────╮
│ {                                                                                                                                                                  │
│   "images": [],                                                                                                                                                    │
│   "text": "a black cat",                                                                                                                                           │
│   "aspect": "16:9",                                                                                                                                                │
│   "style": "raw",                                                                                                                                                  │
│   "stylize": "200"                                                                                                                                                 │
│ }                                                                                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────── Raw Prompt 2 ───────────────────────────────────────────────────────────────────────────╮
│ {                                                                                                                                                                  │
│   "images": [],                                                                                                                                                    │
│   "text": "a blue cat",                                                                                                                                            │
│   "aspect": "16:9",                                                                                                                                                │
│   "style": "raw",                                                                                                                                                  │
│   "stylize": "200"                                                                                                                                                 │
│ }                                                                                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

# PROBLEM 4

> python -m midjargon "a {black, blue} cat --ar 16:9 --style raw --s 200" -j

NOTHING, NO JSON OUTPUT

