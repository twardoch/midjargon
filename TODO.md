Make a deep analysis of the tests vs. the code. For each check that is failing, before doing any actions, go through all the test failings and analyze them. Give each a priority. CAREFULLY consider whether the TEST MAKES LOGICAL SENSE. If it does, attempt to fix the problem in the code. Otherwise adjust or remove THE TEST. 

Try HARD to figure out why the JSON test is failing. 

HERE IS THE OUTPUT OF RUNNING THE TESTS: 


======================================================================== test session starts =========================================================================
platform darwin -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0 -- /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon
configfile: pytest.ini
testpaths: tests
plugins: cov-6.0.0
collected 66 items                                                                                                                                                   

tests/cli/test_main.py::test_basic_prompt FAILED                                                                                                               [  1%]
tests/cli/test_main.py::test_permutations FAILED                                                                                                               [  3%]
tests/cli/test_main.py::test_raw_output FAILED                                                                                                                 [  4%]
tests/cli/test_main.py::test_json_output_formatting FAILED                                                                                                     [  6%]
tests/cli/test_main.py::test_invalid_input FAILED                                                                                                              [  7%]
tests/cli/test_main.py::test_parameter_validation FAILED                                                                                                       [  9%]
tests/cli/test_main.py::test_image_url_handling FAILED                                                                                                         [ 10%]
tests/cli/test_main.py::test_no_color_output FAILED                                                                                                            [ 12%]
tests/cli/test_main.py::test_complex_prompt FAILED                                                                                                             [ 13%]
tests/core/test_input.py::test_basic_input PASSED                                                                                                              [ 15%]
tests/core/test_input.py::test_single_permutation PASSED                                                                                                       [ 16%]
tests/core/test_input.py::test_empty_input FAILED                                                                                                              [ 18%]
tests/core/test_input.py::test_multiple_permutations PASSED                                                                                                    [ 19%]
tests/core/test_input.py::test_nested_permutations PASSED                                                                                                      [ 21%]
tests/core/test_input.py::test_escaped_braces PASSED                                                                                                           [ 22%]
tests/core/test_input.py::test_escaped_commas PASSED                                                                                                           [ 24%]
tests/core/test_input.py::test_unmatched_braces PASSED                                                                                                         [ 25%]
tests/core/test_input.py::test_empty_permutation PASSED                                                                                                        [ 27%]
tests/core/test_input.py::test_whitespace_handling PASSED                                                                                                      [ 28%]
tests/core/test_parameters.py::test_basic_parameter_parsing PASSED                                                                                             [ 30%]
tests/core/test_parameters.py::test_flag_parameters PASSED                                                                                                     [ 31%]
tests/core/test_parameters.py::test_parameter_with_multiple_values PASSED                                                                                      [ 33%]
tests/core/test_parameters.py::test_parameter_with_spaces PASSED                                                                                               [ 34%]
tests/core/test_parameters.py::test_mixed_parameters PASSED                                                                                                    [ 36%]
tests/core/test_parameters.py::test_shorthand_parameters PASSED                                                                                                [ 37%]
tests/core/test_parameters.py::test_niji_version_parameter PASSED                                                                                              [ 39%]
tests/core/test_parameters.py::test_version_parameter PASSED                                                                                                   [ 40%]
tests/core/test_parameters.py::test_personalization_parameter PASSED                                                                                           [ 42%]
tests/core/test_parameters.py::test_reference_parameters PASSED                                                                                                [ 43%]
tests/core/test_parameters.py::test_parameter_order PASSED                                                                                                     [ 45%]
tests/core/test_parameters.py::test_invalid_parameters FAILED                                                                                                  [ 46%]
tests/core/test_permutations.py::test_simple_permutation PASSED                                                                                                [ 48%]
tests/core/test_permutations.py::test_multiple_permutations PASSED                                                                                             [ 50%]
tests/core/test_permutations.py::test_nested_permutations PASSED                                                                                               [ 51%]
tests/core/test_permutations.py::test_escaped_characters PASSED                                                                                                [ 53%]
tests/core/test_permutations.py::test_empty_options PASSED                                                                                                     [ 54%]
tests/core/test_permutations.py::test_single_option PASSED                                                                                                     [ 56%]
tests/core/test_permutations.py::test_split_permutation_options PASSED                                                                                         [ 57%]
tests/core/test_permutations.py::test_invalid_permutations PASSED                                                                                              [ 59%]
tests/core/test_permutations.py::test_permutations_with_parameters PASSED                                                                                      [ 60%]
tests/core/test_permutations.py::test_complex_nested_permutations PASSED                                                                                       [ 62%]
tests/engines/midjourney/test_parser.py::test_numeric_parameters PASSED                                                                                        [ 63%]
tests/engines/midjourney/test_parser.py::test_style_parameters PASSED                                                                                          [ 65%]
tests/engines/midjourney/test_parser.py::test_aspect_ratio PASSED                                                                                              [ 66%]
tests/engines/midjourney/test_parser.py::test_image_prompts PASSED                                                                                             [ 68%]
tests/engines/midjourney/test_parser.py::test_extra_parameters FAILED                                                                                          [ 69%]
tests/engines/midjourney/test_parser.py::test_parameter_conversion PASSED                                                                                      [ 71%]
tests/engines/midjourney/test_parser.py::test_invalid_values PASSED                                                                                            [ 72%]
tests/engines/midjourney/test_parser.py::test_parameter_ranges PASSED                                                                                          [ 74%]
tests/engines/midjourney/test_parser.py::test_empty_values PASSED                                                                                              [ 75%]
tests/engines/midjourney/test_parser.py::test_niji_parameter PASSED                                                                                            [ 77%]
tests/engines/test_base.py::test_engine_parsing PASSED                                                                                                         [ 78%]
tests/engines/test_base.py::test_prompt_to_string PASSED                                                                                                       [ 80%]
tests/engines/test_base.py::test_engine_validation PASSED                                                                                                      [ 81%]
tests/engines/test_base.py::test_engine_with_empty_prompt FAILED                                                                                               [ 83%]
tests/engines/test_base.py::test_engine_with_complex_prompt PASSED                                                                                             [ 84%]
tests/engines/test_base.py::test_engine_roundtrip PASSED                                                                                                       [ 86%]
tests/integration/test_workflow.py::test_basic_workflow PASSED                                                                                                 [ 87%]
tests/integration/test_workflow.py::test_permutation_workflow PASSED                                                                                           [ 89%]
tests/integration/test_workflow.py::test_image_workflow PASSED                                                                                                 [ 90%]
tests/integration/test_workflow.py::test_parameter_workflow FAILED                                                                                             [ 92%]
tests/integration/test_workflow.py::test_new_parameters_workflow FAILED                                                                                        [ 93%]
tests/integration/test_workflow.py::test_weighted_prompts_workflow PASSED                                                                                      [ 95%]
tests/integration/test_workflow.py::test_error_workflow PASSED                                                                                                 [ 96%]
tests/integration/test_workflow.py::test_complex_workflow PASSED                                                                                               [ 98%]
tests/test_package.py::test_version PASSED                                                                                                                     [100%]/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/.venv/lib/python3.13/site-packages/coverage/inorout.py:508: CoverageWarning: Module tests was never imported. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported")


============================================================================== FAILURES ==============================================================================
_________________________________________________________________________ test_basic_prompt __________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x104bc5e40>

    def test_basic_prompt(capture_stdout):
        """Test basic prompt processing."""
        main(f"a beautiful landscape --ar {ASPECT_WIDTH}:{ASPECT_HEIGHT}", json_output=True)
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:68: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        try:
            # Strip any leading/trailing whitespace
            output = output.strip()
            if not output:
                msg = "No JSON found in output"
>               raise ValueError(msg)
E               ValueError: No JSON found in output

tests/cli/test_main.py:57: ValueError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
[
  {
    "text": "a beautiful landscape",
    "image_prompts": [],
    "stylize": null,
    "chaos": null,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": 16,
    "aspect_height": 9,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  }
]
_________________________________________________________________________ test_permutations __________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x104bc7580>

    def test_permutations(capture_stdout):
        """Test permutation processing."""
        main("a {red, blue} bird", json_output=True)
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:81: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        try:
            # Strip any leading/trailing whitespace
            output = output.strip()
            if not output:
                msg = "No JSON found in output"
>               raise ValueError(msg)
E               ValueError: No JSON found in output

tests/cli/test_main.py:57: ValueError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
[
  {
    "text": "a red bird",
    "image_prompts": [],
    "stylize": null,
    "chaos": null,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": null,
    "aspect_height": null,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  },
  {
    "text": "a blue bird",
    "image_prompts": [],
    "stylize": null,
    "chaos": null,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": null,
    "aspect_height": null,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  }
]
__________________________________________________________________________ test_raw_output ___________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x104bc7a00>

    def test_raw_output(capture_stdout):
        """Test raw output mode."""
        main(f"a photo --stylize {STYLIZE_VALUE}", raw=True, json_output=True)
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:92: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        try:
            # Strip any leading/trailing whitespace
            output = output.strip()
            if not output:
                msg = "No JSON found in output"
>               raise ValueError(msg)
E               ValueError: No JSON found in output

tests/cli/test_main.py:57: ValueError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
[
  {
    "images": [],
    "text": "a photo",
    "stylize": 100
  }
]
____________________________________________________________________ test_json_output_formatting _____________________________________________________________________

capture_stdout = <_io.StringIO object at 0x104bc7d00>

    def test_json_output_formatting(capture_stdout):
        """Test JSON output formatting."""
        main("a photo", json_output=True)
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:104: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        try:
            # Strip any leading/trailing whitespace
            output = output.strip()
            if not output:
                msg = "No JSON found in output"
>               raise ValueError(msg)
E               ValueError: No JSON found in output

tests/cli/test_main.py:57: ValueError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
[
  {
    "text": "a photo",
    "image_prompts": [],
    "stylize": null,
    "chaos": null,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": null,
    "aspect_height": null,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  }
]
_________________________________________________________________________ test_invalid_input _________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x104bc5cc0>

    def test_invalid_input(capture_stdout):
        """Test handling of invalid input."""
        with pytest.raises(SystemExit):
            main("", json_output=True)
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:114: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        try:
            # Strip any leading/trailing whitespace
            output = output.strip()
            if not output:
                msg = "No JSON found in output"
>               raise ValueError(msg)
E               ValueError: No JSON found in output

tests/cli/test_main.py:57: ValueError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
{
  "error": "Empty prompt"
}
_____________________________________________________________________ test_parameter_validation ______________________________________________________________________

capture_stdout = <_io.StringIO object at 0x104bc5840>

    def test_parameter_validation(capture_stdout):
        """Test parameter validation."""
        with pytest.raises(SystemExit):
            main(f"a photo --stylize {STYLIZE_VALUE * 20}", json_output=True)  # Over max
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:123: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        try:
            # Strip any leading/trailing whitespace
            output = output.strip()
            if not output:
                msg = "No JSON found in output"
>               raise ValueError(msg)
E               ValueError: No JSON found in output

tests/cli/test_main.py:57: ValueError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
{
  "error": "Invalid numeric value for stylize: 2000"
}
______________________________________________________________________ test_image_url_handling _______________________________________________________________________

capture_stdout = <_io.StringIO object at 0x104de41c0>

    def test_image_url_handling(capture_stdout):
        """Test handling of image URLs."""
        url = "https://example.com/image.jpg"
        main(f"{url} a fusion", json_output=True)
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:132: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        try:
            # Strip any leading/trailing whitespace
            output = output.strip()
            if not output:
                msg = "No JSON found in output"
>               raise ValueError(msg)
E               ValueError: No JSON found in output

tests/cli/test_main.py:57: ValueError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
[
  {
    "text": "a fusion",
    "image_prompts": [
      {
        "url": "https://example.com/image.jpg"
      }
    ],
    "stylize": null,
    "chaos": null,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": null,
    "aspect_height": null,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  }
]
________________________________________________________________________ test_no_color_output ________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x104bc7580>

    def test_no_color_output(capture_stdout):
        """Test no-color output mode."""
        Console(force_terminal=False)
        main("a photo", json_output=True)
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:146: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        try:
            # Strip any leading/trailing whitespace
            output = output.strip()
            if not output:
                msg = "No JSON found in output"
>               raise ValueError(msg)
E               ValueError: No JSON found in output

tests/cli/test_main.py:57: ValueError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
[
  {
    "text": "a photo",
    "image_prompts": [],
    "stylize": null,
    "chaos": null,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": null,
    "aspect_height": null,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  }
]
________________________________________________________________________ test_complex_prompt _________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x104bc7a00>

    def test_complex_prompt(capture_stdout):
        """Test complex prompt with multiple features."""
        prompt = (
            "https://example.com/img1.jpg https://example.com/img2.jpg "
            "a {red, blue} bird on a {branch, rock} "
            f"--ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE} --chaos {CHAOS_VALUE}"
        )
        main(prompt, json_output=True)
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:160: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        try:
            # Strip any leading/trailing whitespace
            output = output.strip()
            if not output:
                msg = "No JSON found in output"
>               raise ValueError(msg)
E               ValueError: No JSON found in output

tests/cli/test_main.py:57: ValueError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
[
  {
    "text": "a red bird on a branch",
    "image_prompts": [
      {
        "url": "https://example.com/img1.jpg"
      },
      {
        "url": "https://example.com/img2.jpg"
      }
    ],
    "stylize": 100,
    "chaos": 50,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": 16,
    "aspect_height": 9,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  },
  {
    "text": "a red bird on a rock",
    "image_prompts": [
      {
        "url": "https://example.com/img1.jpg"
      },
      {
        "url": "https://example.com/img2.jpg"
      }
    ],
    "stylize": 100,
    "chaos": 50,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": 16,
    "aspect_height": 9,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  },
  {
    "text": "a blue bird on a branch",
    "image_prompts": [
      {
        "url": "https://example.com/img1.jpg"
      },
      {
        "url": "https://example.com/img2.jpg"
      }
    ],
    "stylize": 100,
    "chaos": 50,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": 16,
    "aspect_height": 9,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  },
  {
    "text": "a blue bird on a rock",
    "image_prompts": [
      {
        "url": "https://example.com/img1.jpg"
      },
      {
        "url": "https://example.com/img2.jpg"
      }
    ],
    "stylize": 100,
    "chaos": 50,
    "weird": null,
    "image_weight": null,
    "seed": null,
    "stop": null,
    "aspect_width": 16,
    "aspect_height": 9,
    "style": null,
    "version": null,
    "personalization": null,
    "quality": null,
    "character_reference": [],
    "character_weight": null,
    "style_reference": [],
    "style_weight": null,
    "style_version": null,
    "repeat": null,
    "turbo": false,
    "relax": false,
    "tile": false,
    "negative_prompt": null,
    "extra_params": {}
  }
]
__________________________________________________________________________ test_empty_input __________________________________________________________________________

    def test_empty_input():
        """Test empty input handling."""
>       result = expand_midjargon_input("")

tests/core/test_input.py:32: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

prompt = ''

    def expand_midjargon_input(prompt: MidjargonInput) -> MidjargonList:
        """
        Expands a raw midjargon prompt string into a list of fully expanded prompt strings.
    
        Args:
            prompt: A raw MidjargonInput string that may contain permutation syntax (e.g. {red, blue}).
    
        Returns:
            A list of MidjargonPrompt strings with all permutation expressions resolved.
    
        Raises:
            ValueError: If the prompt is empty or invalid.
        """
        if not prompt.strip():
            msg = "Empty prompt"
>           raise ValueError(msg)
E           ValueError: Empty prompt

src/midjargon/core/input.py:27: ValueError
______________________________________________________________________ test_invalid_parameters _______________________________________________________________________

    def test_invalid_parameters():
        """Test handling of invalid parameter formats."""
        with pytest.raises(ValueError):
            parse_parameters("--")  # Empty parameter name
    
        with pytest.raises(ValueError):
            parse_parameters("--ar")  # Missing required value
    
        with pytest.raises(ValueError):
            parse_parameters("ar 16:9")  # Missing -- prefix
    
        with pytest.raises(ValueError):
            parse_parameters("--v")  # Missing version value
    
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/core/test_parameters.py:129: Failed
_______________________________________________________________________ test_extra_parameters ________________________________________________________________________

    def test_extra_parameters():
        """Test handling of unknown parameters."""
        parser = MidjourneyParser()
>       prompt = parser.parse_dict(
            {
                "text": "a photo",
                "unknown": "value",
                "flag": None,
            }
        )

tests/engines/midjourney/test_parser.py:77: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x104d75fd0>, midjargon_dict = {'flag': None, 'text': 'a photo', 'unknown': 'value'}

    def parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """
        Parse a MidjargonDict into a validated MidjourneyPrompt.
    
        Args:
            midjargon_dict: Dictionary from basic parser.
    
        Returns:
            Validated MidjourneyPrompt.
    
        Raises:
            ValueError: If the prompt text is empty or if validation fails.
        """
        # Validate text is not empty
        text_value = midjargon_dict.get("text")
        if text_value is None:
            msg = "Missing prompt text"
            raise ValueError(msg)
    
        if isinstance(text_value, list):
            text = text_value[0] if text_value else ""
        else:
            text = str(text_value)
    
        if not text.strip():
            msg = "Empty prompt text"
            raise ValueError(msg)
    
        # Initialize with core components
        images = midjargon_dict.get("images", [])
        if images is None:
            images = []
    
        prompt_data: dict[str, Any] = {
            "text": text,
            "image_prompts": [ImagePrompt(url=url) for url in images],
            "extra_params": {},
            "version": None,
            "personalization": None,
            "style": None,
        }
    
        # Process each parameter
        for name, value in midjargon_dict.items():
            if name in ("text", "images"):
                continue
    
            # Try numeric parameters first
            param_name, param_value = self._handle_numeric_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle aspect ratio
            if name in ("ar", "aspect"):
                w, h = self._handle_aspect_ratio(value)
                if w is not None and h is not None:
                    prompt_data["aspect_width"] = w
                    prompt_data["aspect_height"] = h
                continue
    
            # Handle version parameter for keys 'v', 'version', and 'niji'
            if name in ("v", "version", "niji"):
                param_name, param_value = self._handle_version_param(name, value)
                if param_name:
                    # Only update version if not already set by --v
                    if not (
                        name == "niji"
                        and prompt_data["version"]
                        and prompt_data["version"].startswith("v")
                    ):
                        prompt_data[param_name] = param_value
                continue
    
            # Handle style parameter
            param_name, param_value = self._handle_style_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle personalization parameter
            param_name, param_value = self._handle_personalization_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle negative prompt
            param_name, param_value = self._handle_negative_prompt(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle reference parameter
            param_name, param_value = self._handle_reference_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle boolean flags
            if name in ("turbo", "relax", "tile"):
                if value is None:
                    prompt_data[name] = True
                else:
                    norm_value = self._normalize_value(value)
                    if isinstance(norm_value, list):
                        norm_value = norm_value[0] if norm_value else None
                    if norm_value is not None:
                        norm_str = str(norm_value).lower()
                        prompt_data[name] = norm_str == "true"
                    else:
                        prompt_data[name] = False
                continue
    
            # Store unknown parameters
            prompt_data["extra_params"][name] = value
    
        # Create and validate prompt
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       style
E         Value error, Invalid style value. Must be one of: {'cute', 'scenic', 'raw', 'expressive', 'original'} [type=value_error, input_value='value', input_type=str]
E           For further information visit https://errors.pydantic.dev/2.10/v/value_error

src/midjargon/engines/midjourney/parser.py:399: ValidationError
___________________________________________________________________ test_engine_with_empty_prompt ____________________________________________________________________

    def test_engine_with_empty_prompt():
        """Test engine handling of empty prompt."""
        engine = TestEngine()
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/engines/test_base.py:69: Failed
______________________________________________________________________ test_parameter_workflow _______________________________________________________________________

    def test_parameter_workflow():
        """Test workflow with various parameter types."""
        prompt = (
            "cyberpunk city --v 5.2 --style raw --niji 6 "
            f"--chaos {CHAOS_VALUE} --weird {WEIRD_VALUE} "
            f"--seed {SEED_VALUE} --stop {STOP_VALUE} "
            "--turbo --tile"
        )
>       results = process_prompt(prompt)

tests/integration/test_workflow.py:100: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/integration/test_workflow.py:40: in process_prompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x104509400>, midjargon_dict = {'chaos': 50, 'images': [], 'seed': 12345, 'stop': 80, ...}

    def parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """
        Parse a MidjargonDict into a validated MidjourneyPrompt.
    
        Args:
            midjargon_dict: Dictionary from basic parser.
    
        Returns:
            Validated MidjourneyPrompt.
    
        Raises:
            ValueError: If the prompt text is empty or if validation fails.
        """
        # Validate text is not empty
        text_value = midjargon_dict.get("text")
        if text_value is None:
            msg = "Missing prompt text"
            raise ValueError(msg)
    
        if isinstance(text_value, list):
            text = text_value[0] if text_value else ""
        else:
            text = str(text_value)
    
        if not text.strip():
            msg = "Empty prompt text"
            raise ValueError(msg)
    
        # Initialize with core components
        images = midjargon_dict.get("images", [])
        if images is None:
            images = []
    
        prompt_data: dict[str, Any] = {
            "text": text,
            "image_prompts": [ImagePrompt(url=url) for url in images],
            "extra_params": {},
            "version": None,
            "personalization": None,
            "style": None,
        }
    
        # Process each parameter
        for name, value in midjargon_dict.items():
            if name in ("text", "images"):
                continue
    
            # Try numeric parameters first
            param_name, param_value = self._handle_numeric_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle aspect ratio
            if name in ("ar", "aspect"):
                w, h = self._handle_aspect_ratio(value)
                if w is not None and h is not None:
                    prompt_data["aspect_width"] = w
                    prompt_data["aspect_height"] = h
                continue
    
            # Handle version parameter for keys 'v', 'version', and 'niji'
            if name in ("v", "version", "niji"):
                param_name, param_value = self._handle_version_param(name, value)
                if param_name:
                    # Only update version if not already set by --v
                    if not (
                        name == "niji"
                        and prompt_data["version"]
                        and prompt_data["version"].startswith("v")
                    ):
                        prompt_data[param_name] = param_value
                continue
    
            # Handle style parameter
            param_name, param_value = self._handle_style_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle personalization parameter
            param_name, param_value = self._handle_personalization_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle negative prompt
            param_name, param_value = self._handle_negative_prompt(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle reference parameter
            param_name, param_value = self._handle_reference_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle boolean flags
            if name in ("turbo", "relax", "tile"):
                if value is None:
                    prompt_data[name] = True
                else:
                    norm_value = self._normalize_value(value)
                    if isinstance(norm_value, list):
                        norm_value = norm_value[0] if norm_value else None
                    if norm_value is not None:
                        norm_str = str(norm_value).lower()
                        prompt_data[name] = norm_str == "true"
                    else:
                        prompt_data[name] = False
                continue
    
            # Store unknown parameters
            prompt_data["extra_params"][name] = value
    
        # Create and validate prompt
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       version
E         Value error, Invalid version value. Must be one of: {'6.1', '5.1', '5.0', '5.2', '4', '5', '6', '1', '2', '3'} [type=value_error, input_value='vniji 6', input_type=str]
E           For further information visit https://errors.pydantic.dev/2.10/v/value_error

src/midjargon/engines/midjourney/parser.py:399: ValidationError
____________________________________________________________________ test_new_parameters_workflow ____________________________________________________________________

    def test_new_parameters_workflow():
        """Test workflow with new parameter types."""
        prompt = (
            "portrait photo "
            f"--quality {QUALITY_VALUE} "
            f"--cw {CHARACTER_WEIGHT_VALUE} "
            f"--sw {STYLE_WEIGHT_VALUE} "
            f"--sv {STYLE_VERSION_VALUE} "
            f"--repeat {REPEAT_VALUE} "
            "--cref ref1.jpg "
            "--sref style1.jpg,style2.jpg "
            "--p custom_profile"
        )
>       results = process_prompt(prompt)

tests/integration/test_workflow.py:129: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/integration/test_workflow.py:40: in process_prompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x104509400>
midjargon_dict = {'character_reference': 'ref1.jpg', 'character_weight': 100, 'images': [], 'personalization': 'custom_profile', ...}

    def parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """
        Parse a MidjargonDict into a validated MidjourneyPrompt.
    
        Args:
            midjargon_dict: Dictionary from basic parser.
    
        Returns:
            Validated MidjourneyPrompt.
    
        Raises:
            ValueError: If the prompt text is empty or if validation fails.
        """
        # Validate text is not empty
        text_value = midjargon_dict.get("text")
        if text_value is None:
            msg = "Missing prompt text"
            raise ValueError(msg)
    
        if isinstance(text_value, list):
            text = text_value[0] if text_value else ""
        else:
            text = str(text_value)
    
        if not text.strip():
            msg = "Empty prompt text"
            raise ValueError(msg)
    
        # Initialize with core components
        images = midjargon_dict.get("images", [])
        if images is None:
            images = []
    
        prompt_data: dict[str, Any] = {
            "text": text,
            "image_prompts": [ImagePrompt(url=url) for url in images],
            "extra_params": {},
            "version": None,
            "personalization": None,
            "style": None,
        }
    
        # Process each parameter
        for name, value in midjargon_dict.items():
            if name in ("text", "images"):
                continue
    
            # Try numeric parameters first
            param_name, param_value = self._handle_numeric_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle aspect ratio
            if name in ("ar", "aspect"):
                w, h = self._handle_aspect_ratio(value)
                if w is not None and h is not None:
                    prompt_data["aspect_width"] = w
                    prompt_data["aspect_height"] = h
                continue
    
            # Handle version parameter for keys 'v', 'version', and 'niji'
            if name in ("v", "version", "niji"):
                param_name, param_value = self._handle_version_param(name, value)
                if param_name:
                    # Only update version if not already set by --v
                    if not (
                        name == "niji"
                        and prompt_data["version"]
                        and prompt_data["version"].startswith("v")
                    ):
                        prompt_data[param_name] = param_value
                continue
    
            # Handle style parameter
            param_name, param_value = self._handle_style_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle personalization parameter
            param_name, param_value = self._handle_personalization_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle negative prompt
            param_name, param_value = self._handle_negative_prompt(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle reference parameter
            param_name, param_value = self._handle_reference_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle boolean flags
            if name in ("turbo", "relax", "tile"):
                if value is None:
                    prompt_data[name] = True
                else:
                    norm_value = self._normalize_value(value)
                    if isinstance(norm_value, list):
                        norm_value = norm_value[0] if norm_value else None
                    if norm_value is not None:
                        norm_str = str(norm_value).lower()
                        prompt_data[name] = norm_str == "true"
                    else:
                        prompt_data[name] = False
                continue
    
            # Store unknown parameters
            prompt_data["extra_params"][name] = value
    
        # Create and validate prompt
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       style
E         Value error, Invalid style value. Must be one of: {'cute', 'scenic', 'raw', 'expressive', 'original'} [type=value_error, input_value='custom_profile', input_type=str]
E           For further information visit https://errors.pydantic.dev/2.10/v/value_error

src/midjargon/engines/midjourney/parser.py:399: ValidationError
========================================================================== warnings summary ==========================================================================
tests/engines/test_base.py:14
  /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/tests/engines/test_base.py:14: PytestCollectionWarning: cannot collect test class 'TestPrompt' because it has a __init__ constructor (from: tests/engines/test_base.py)
    class TestPrompt(BaseModel):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================================================== slowest 10 durations ========================================================================

(10 durations < 0.005s hidden.  Use -vv to show these durations.)
====================================================================== short test summary info =======================================================================
FAILED tests/cli/test_main.py::test_basic_prompt - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_permutations - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_raw_output - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_json_output_formatting - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_invalid_input - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_parameter_validation - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_image_url_handling - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_no_color_output - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_complex_prompt - ValueError: No JSON found in output
FAILED tests/core/test_input.py::test_empty_input - ValueError: Empty prompt
FAILED tests/core/test_parameters.py::test_invalid_parameters - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/engines/midjourney/test_parser.py::test_extra_parameters - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
FAILED tests/engines/test_base.py::test_engine_with_empty_prompt - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/integration/test_workflow.py::test_parameter_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
FAILED tests/integration/test_workflow.py::test_new_parameters_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
============================================================== 15 failed, 51 passed, 1 warning in 0.87s ==============================================================