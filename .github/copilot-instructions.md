
Maintain a `this_file` record in all source files to track their relative path from the project root: for **Python/Shell/TOML** files, use `# this_file: path/from/root.ext` as the first comment (after any shebang line `#!`), and for **Markdown** files, include `this_file: path/from/root.md` in the YAML front matter block at the document start. Update paths when moving files. Keep the entry as the first metadata element. Use Unix-style `/` path separators. Omit leading `./` in paths. *Example:* A Python file in `src/utils` would start with `#!/usr/bin/env python3\n# this_file: src/utils/helpers.py`.

# `midjargon`

`midjargon` is a hatch-managed Python library for parsing and manipulating Midjourney prompts using a specialized syntax. This tool helps you work with Midjourney prompts in a structured way, handling complex features like permutations, parameter validation, and image URL extraction.

<guidelines for python>
1. WHEN YOU WRITE PYTHON: 

a. CORE STYLE: Follow PEP 8 for consistent formatting & naming. Write clear, descriptive names for functions & variables. Keep code simple & explicit (PEP 20). Prioritize readability over cleverness. 
b. MODERN FEATURES: Use type hints in their simplest form (list, dict, | for unions). Write clear, imperative docstrings (PEP 257). Employ f-strings for string formatting. Use structural pattern matching where appropriate. 
c. CODE STRUCTURE: Extract repeated logic into focused functions. Handle errors explicitly and gracefully. Keep functions small and single-purpose. Prefer flat over nested structures. 
d. LIBRARIES (when needed): pathlib for file operations, pydantic for data validation, loguru for logging. Write maintainable code that future developers can easily understand and modify. 
e. If the script is for CLI execution, use fire for CLI, rich for enhanced console output, and ensure that the script starts with the `uv` shebang and metadata like shown below where `[...]` is a list of Python dependency specifiers, like `["fire", "rich"]`: 

```
#!/usr/bin/env -S uv run 
# /// script
# dependencies = [...]
# ///
```

f. The above only applies if I ask you explicitly to write Python or if you're editing existing Python code.
</guidelines>
<work>
<step 1: analysis>
Make an in-depth critical analysis of the `TASK` presented to you. Read the content of the @TODO.md file (in the project workspace dir) to see the current state of progress of the TASK. Then make an in-depth critical analysis of the inputs presented. 
</step>
<step 2: gather up-to-date insights>
Consult the @Web if you can. Consult the most up-to-date @Docs and run `sh updateme.sh`. 
</step>
<step 3: plan>Think carefully about your plan to achieve the goal, following the provided guidelines. Write out general principles, then propose specific changes. 
</step>
<step 4: pre-implementation>
Once you’ve analyzed the TASK request and the inputs, you’ve gathered up-to-date insights and ran the `hatch` tests and checks and once you’ve made a careful plan — write the entire plan into the file @LOG.md (in the project workspace folder) — be very detailed and specific. 
</step>
<step 5: implementation>
You can start implementing the plan. Whenever you’ve made larger edits to Python files, run `sh updateme.sh` to see how your changes impacted the @Codebase , then refine your plan. Keep progress documentation in @LOG.md (in the project workspace folder) , remove completed items. Work until you CLEAR the @TODO.md !     
</step>
</work>

