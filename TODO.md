Here’s a summary of my review of the failing tests and some thoughts on which ones might not logically make sense:

1. Permutation expansion tests (e.g. test_single_permutation, test_multiple_permutations, test_whitespace_handling, test_empty_permutation, test_single_option, test_nested_permutations, etc.):
  • All of these tests expect that when you write a prompt like "a {red, blue} bird" the expansion should yield results like "a red bird" and "a blue bird" (i.e. with a space between “red” and “bird”). Yet the actual output is “a redbird” (no space between the expanded option and the following text).  
  • This repeated expectation for an extra space in the output is dubious. When writing a prompt, if the input literally includes spaces around the permutation (for example, "a {  red  ,  blue  } bird"), one might expect trimming of spaces within options—but then the joining logic should not “collapse” the space between the fixed text and the option. In many cases, the tests assume the code will inject a space (e.g. “a red bird”), even though in the literal concatenation it might be more natural to produce “a redbird” if the input isn’t handled carefully. In other words, there is an inconsistency here: either the code should be smart about joining words (inserting spaces when needed) or the tests should match a “literal” expansion.  
  • Similarly, tests for escaped commas and escaped braces (test_escaped_commas and test_escaped_braces) have expectations that seem off. For example, in test_escaped_braces the input is r"a \{red, blue\} bird" but the expected result is "{red, blue} bird"—omitting the “a ” that’s in the literal input. That expectation does not match a typical “escape” handling (we’d expect the escape to simply remove the backslashes, preserving the literal text).  
  • The empty permutation test (test_empty_permutation) expects "a  bird" (with two spaces) when given "a {} bird" but the actual output is "abird". Typically, if an empty option is detected one might simply remove it and join consistently (resulting in “abird” might be acceptable) unless the spec explicitly says “insert an extra space.” Overall, these permutation-related tests appear to have inconsistent (and perhaps nonintentional) expectations.

2. CLI output tests (tests/cli/test_main.py):
  • Several tests (test_basic_prompt, test_raw_output, test_complex_prompt, etc.) expect that when the main function is called with json_output=True the output will contain valid JSON (or at least a JSON token like "{" or "[" somewhere in the string). However, in every case the captured output is empty or just the formatted console output (possibly with color formatting or extra decoration), so the tests conclude “No JSON found in output.”  
  • If the CLI is intended to support both human-readable (colored/structured) and JSON output, the tests should clearly separate these modes; otherwise, expecting JSON when it isn’t actually produced doesn’t make sense.

3. Parameter parsing tests (tests/core/test_parameters.py):
  • For example, test_version_parameter expects that when you set "--v 5.2", the parsed version ends up being "5.2". Instead, it’s coming through as "v5.2" (with a leading “v”). It’s unclear which behavior is “correct” from a design standpoint, but the test’s expectation may not align with the intended shorthand behavior.
  • Similarly, test_invalid_parameters expects a ValueError for certain malformed parameter formats, but no error is raised. Either the validation should be made stricter or the test’s assumption of what’s “invalid” should be revisited.

4. Engine and workflow tests (tests/engines/* and tests/integration/*):
  • test_engine_with_empty_prompt expects a ValueError when an empty prompt is passed to the engine, yet no error occurs. Given that lower-level functions (like expand_midjargon_input) already raise an error on empty prompts, it seems odd that the engine wouldn’t propagate or check for this condition.
  • In test_new_parameters_workflow the test provides a --cref parameter and expects the character_reference to include that file name, but the parsed result is empty. That discrepancy suggests either the test or the parsing logic is off.
  • test_error_workflow expects several errors for invalid inputs (e.g. malformed parameters or invalid image URL), yet not all of these conditions trigger an error. Either the error handling in the workflow isn’t complete, or the tests have unreasonable expectations.

In summary, while some failures clearly indicate bugs (such as missing spaces in permutation expansion or incorrect handling of escapes), several tests seem to have expectations that don’t match a “logical” interpretation of the input:
  – The assumption that the parser should magically insert extra spaces (e.g. “a red bird” vs. “a redbird”) is questionable.
  – The handling of escape sequences (braces and commas) in tests appears inconsistent with the literal input.
  – Expecting JSON output when the CLI might be designed to deliver a more decorated (and possibly non‐JSON) output may be a mismatch.
  – Parameter parsing tests assume a stripped version (e.g. "5.2") even though the shorthand may intentionally include a “v” prefix.

These observations suggest that some of the tests might not logically make sense relative to the intended design, and it would be worth clarifying the specification for:

> How exactly permutation strings should be joined (should spaces be auto-inserted?),

`a{b, c}d` should expand to `abd` `acd`. The spaces right around the `{` and `}` should be treated as they are. Spaces around the separating commas can be collapsed fully, as if there is no space.

> How escapes should work (do we preserve literal text exactly?),

\{ \} \, must work

> What the CLI output format should be when json_output is requested

List of dicts

> How parameters (like version) should be normalized.

Not really normalized, keep as strings unless it’s obviously int or float. Version "number" should be kept a string.


TASK: ADDRESS THE PROBLEMS MENTIONED ABOVE

===============================================================================================================================================================================

BELOW IS THE FULL TEST REPORT

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
tests/core/test_input.py::test_single_permutation FAILED                                                                                                       [ 16%]
tests/core/test_input.py::test_empty_input FAILED                                                                                                              [ 18%]
tests/core/test_input.py::test_multiple_permutations FAILED                                                                                                    [ 19%]
tests/core/test_input.py::test_nested_permutations PASSED                                                                                                      [ 21%]
tests/core/test_input.py::test_escaped_braces FAILED                                                                                                           [ 22%]
tests/core/test_input.py::test_escaped_commas FAILED                                                                                                           [ 24%]
tests/core/test_input.py::test_unmatched_braces PASSED                                                                                                         [ 25%]
tests/core/test_input.py::test_empty_permutation FAILED                                                                                                        [ 27%]
tests/core/test_input.py::test_whitespace_handling FAILED                                                                                                      [ 28%]
tests/core/test_parameters.py::test_basic_parameter_parsing PASSED                                                                                             [ 30%]
tests/core/test_parameters.py::test_flag_parameters PASSED                                                                                                     [ 31%]
tests/core/test_parameters.py::test_parameter_with_multiple_values PASSED                                                                                      [ 33%]
tests/core/test_parameters.py::test_parameter_with_spaces PASSED                                                                                               [ 34%]
tests/core/test_parameters.py::test_mixed_parameters PASSED                                                                                                    [ 36%]
tests/core/test_parameters.py::test_shorthand_parameters PASSED                                                                                                [ 37%]
tests/core/test_parameters.py::test_niji_version_parameter PASSED                                                                                              [ 39%]
tests/core/test_parameters.py::test_version_parameter FAILED                                                                                                   [ 40%]
tests/core/test_parameters.py::test_personalization_parameter PASSED                                                                                           [ 42%]
tests/core/test_parameters.py::test_reference_parameters PASSED                                                                                                [ 43%]
tests/core/test_parameters.py::test_parameter_order PASSED                                                                                                     [ 45%]
tests/core/test_parameters.py::test_invalid_parameters FAILED                                                                                                  [ 46%]
tests/core/test_permutations.py::test_simple_permutation FAILED                                                                                                [ 48%]
tests/core/test_permutations.py::test_multiple_permutations FAILED                                                                                             [ 50%]
tests/core/test_permutations.py::test_nested_permutations FAILED                                                                                               [ 51%]
tests/core/test_permutations.py::test_escaped_characters FAILED                                                                                                [ 53%]
tests/core/test_permutations.py::test_empty_options FAILED                                                                                                     [ 54%]
tests/core/test_permutations.py::test_single_option FAILED                                                                                                     [ 56%]
tests/core/test_permutations.py::test_split_permutation_options PASSED                                                                                         [ 57%]
tests/core/test_permutations.py::test_invalid_permutations FAILED                                                                                              [ 59%]
tests/core/test_permutations.py::test_permutations_with_parameters PASSED                                                                                      [ 60%]
tests/core/test_permutations.py::test_complex_nested_permutations FAILED                                                                                       [ 62%]
tests/engines/midjourney/test_parser.py::test_numeric_parameters PASSED                                                                                        [ 63%]
tests/engines/midjourney/test_parser.py::test_style_parameters PASSED                                                                                          [ 65%]
tests/engines/midjourney/test_parser.py::test_aspect_ratio PASSED                                                                                              [ 66%]
tests/engines/midjourney/test_parser.py::test_image_prompts PASSED                                                                                             [ 68%]
tests/engines/midjourney/test_parser.py::test_extra_parameters PASSED                                                                                          [ 69%]
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
tests/integration/test_workflow.py::test_permutation_workflow FAILED                                                                                           [ 89%]
tests/integration/test_workflow.py::test_image_workflow PASSED                                                                                                 [ 90%]
tests/integration/test_workflow.py::test_parameter_workflow FAILED                                                                                             [ 92%]
tests/integration/test_workflow.py::test_new_parameters_workflow FAILED                                                                                        [ 93%]
tests/integration/test_workflow.py::test_weighted_prompts_workflow PASSED                                                                                      [ 95%]
tests/integration/test_workflow.py::test_error_workflow FAILED                                                                                                 [ 96%]
tests/integration/test_workflow.py::test_complex_workflow PASSED                                                                                               [ 98%]
tests/test_package.py::test_version PASSED                                                                                                                     [100%]/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/.venv/lib/python3.13/site-packages/coverage/inorout.py:508: CoverageWarning: Module tests was never imported. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported")


============================================================================== FAILURES ==============================================================================
_________________________________________________________________________ test_basic_prompt __________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x110a4db40>

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
        # Find the first { or [ in the output
        start = output.find("{") if "{" in output else output.find("[")
        if start == -1:
            msg = "No JSON found in output"
>           raise ValueError(msg)
E           ValueError: No JSON found in output

tests/cli/test_main.py:53: ValueError
_________________________________________________________________________ test_permutations __________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x110a4f1c0>

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
        # Find the first { or [ in the output
        start = output.find("{") if "{" in output else output.find("[")
        if start == -1:
            msg = "No JSON found in output"
>           raise ValueError(msg)
E           ValueError: No JSON found in output

tests/cli/test_main.py:53: ValueError
__________________________________________________________________________ test_raw_output ___________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x110a4f580>

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
        # Find the first { or [ in the output
        start = output.find("{") if "{" in output else output.find("[")
        if start == -1:
            msg = "No JSON found in output"
>           raise ValueError(msg)
E           ValueError: No JSON found in output

tests/cli/test_main.py:53: ValueError
____________________________________________________________________ test_json_output_formatting _____________________________________________________________________

capture_stdout = <_io.StringIO object at 0x110a4f100>

    def test_json_output_formatting(capture_stdout):
        """Test JSON output formatting."""
        main("a photo", json_output=True)
        output = capture_stdout.getvalue()
        # Verify it's properly indented JSON
>       assert "\n  " in output  # Check for indentation
E       AssertionError: assert '\n  ' in ''

tests/cli/test_main.py:105: AssertionError
_________________________________________________________________________ test_invalid_input _________________________________________________________________________

capture_stderr = <_io.StringIO object at 0x110a4f640>

    def test_invalid_input(capture_stderr):
        """Test handling of invalid input."""
        with pytest.raises(SystemExit):
            main("", json_output=True)
>       assert "Error" in capture_stderr.getvalue()
E       AssertionError: assert 'Error' in ''
E        +  where '' = <built-in method getvalue of _io.StringIO object at 0x110a4f640>()
E        +    where <built-in method getvalue of _io.StringIO object at 0x110a4f640> = <_io.StringIO object at 0x110a4f640>.getvalue

tests/cli/test_main.py:114: AssertionError
------------------------------------------------------------------------ Captured stderr call ------------------------------------------------------------------------
Error: Empty prompt
_____________________________________________________________________ test_parameter_validation ______________________________________________________________________

capture_stderr = <_io.StringIO object at 0x110a4da80>

    def test_parameter_validation(capture_stderr):
        """Test parameter validation."""
        with pytest.raises(SystemExit):
            main(f"a photo --stylize {STYLIZE_VALUE * 20}", json_output=True)  # Over max
>       assert "Error" in capture_stderr.getvalue()
E       AssertionError: assert 'Error' in ''
E        +  where '' = <built-in method getvalue of _io.StringIO object at 0x110a4da80>()
E        +    where <built-in method getvalue of _io.StringIO object at 0x110a4da80> = <_io.StringIO object at 0x110a4da80>.getvalue

tests/cli/test_main.py:125: AssertionError
------------------------------------------------------------------------ Captured stderr call ------------------------------------------------------------------------
Error: Invalid numeric value for stylize: 2000
______________________________________________________________________ test_image_url_handling _______________________________________________________________________

capture_stdout = <_io.StringIO object at 0x110a4ff40>

    def test_image_url_handling(capture_stdout):
        """Test handling of image URLs."""
        url = "https://example.com/image.jpg"
        main(f"{url} a fusion", json_output=True)
        output = capture_stdout.getvalue()
>       data = parse_json_output(output)

tests/cli/test_main.py:137: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        # Find the first { or [ in the output
        start = output.find("{") if "{" in output else output.find("[")
        if start == -1:
            msg = "No JSON found in output"
>           raise ValueError(msg)
E           ValueError: No JSON found in output

tests/cli/test_main.py:53: ValueError
________________________________________________________________________ test_no_color_output ________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x110bcc400>

    def test_no_color_output(capture_stdout):
        """Test no-color output mode."""
        Console(force_terminal=False)
        main("a photo", no_color=True)
        # Just verify it runs without error, as color testing is complex
>       assert capture_stdout.getvalue()
E       AssertionError: assert ''
E        +  where '' = <built-in method getvalue of _io.StringIO object at 0x110bcc400>()
E        +    where <built-in method getvalue of _io.StringIO object at 0x110bcc400> = <_io.StringIO object at 0x110bcc400>.getvalue

tests/cli/test_main.py:150: AssertionError
------------------------------------------------------------------------ Captured stdout call ------------------------------------------------------------------------
╭───────────────────────────────── Formatted ──────────────────────────────────╮
│ a photo                                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────── Structured ─────────────────────────────────╮
│ {                                                                            │
│   "text": "a photo",                                                         │
│   "image_prompts": [],                                                       │
│   "stylize": null,                                                           │
│   "chaos": null,                                                             │
│   "weird": null,                                                             │
│   "image_weight": null,                                                      │
│   "seed": null,                                                              │
│   "stop": null,                                                              │
│   "aspect_width": null,                                                      │
│   "aspect_height": null,                                                     │
│   "style": null,                                                             │
│   "version": null,                                                           │
│   "personalization": null,                                                   │
│   "quality": null,                                                           │
│   "character_reference": [],                                                 │
│   "character_weight": null,                                                  │
│   "style_reference": [],                                                     │
│   "style_weight": null,                                                      │
│   "style_version": null,                                                     │
│   "repeat": null,                                                            │
│   "turbo": false,                                                            │
│   "relax": false,                                                            │
│   "tile": false,                                                             │
│   "negative_prompt": null,                                                   │
│   "extra_params": {}                                                         │
│ }                                                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
________________________________________________________________________ test_complex_prompt _________________________________________________________________________

capture_stdout = <_io.StringIO object at 0x110a4d900>

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

tests/cli/test_main.py:162: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output = ''

    def parse_json_output(output: str) -> Any:
        """Parse JSON output from the CLI."""
        # Find the first { or [ in the output
        start = output.find("{") if "{" in output else output.find("[")
        if start == -1:
            msg = "No JSON found in output"
>           raise ValueError(msg)
E           ValueError: No JSON found in output

tests/cli/test_main.py:53: ValueError
______________________________________________________________________ test_single_permutation _______________________________________________________________________

    def test_single_permutation():
        """Test input with a single permutation."""
        result = expand_midjargon_input("a {red, blue} bird")
        assert len(result) == PERMUTATION_COUNT_2
>       assert "a red bird" in result
E       AssertionError: assert 'a red bird' in ['a redbird', 'a bluebird']

tests/core/test_input.py:26: AssertionError
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
_____________________________________________________________________ test_multiple_permutations _____________________________________________________________________

    def test_multiple_permutations():
        """Test input with multiple permutations."""
        result = expand_midjargon_input("a {red, blue, green} bird")
        assert len(result) == PERMUTATION_COUNT_3
>       assert "a red bird" in result
E       AssertionError: assert 'a red bird' in ['a redbird', 'a bluebird', 'a greenbird']

tests/core/test_input.py:41: AssertionError
________________________________________________________________________ test_escaped_braces _________________________________________________________________________

    def test_escaped_braces():
        """Test input with escaped braces."""
        result = expand_midjargon_input(r"a \{red, blue\} bird")
        assert len(result) == 1
>       assert result[0] == "{red, blue} bird"
E       AssertionError: assert 'a {red, blue} bird' == '{red, blue} bird'
E         
E         - {red, blue} bird
E         + a {red, blue} bird
E         ? ++

tests/core/test_input.py:59: AssertionError
________________________________________________________________________ test_escaped_commas _________________________________________________________________________

    def test_escaped_commas():
        """Test input with escaped commas."""
        result = expand_midjargon_input(r"a {red\, blue, green} bird")
        assert len(result) == PERMUTATION_COUNT_2
>       assert "a red, blue bird" in result
E       AssertionError: assert 'a red, blue bird' in ['a red\\, bluebird', 'a greenbird']

tests/core/test_input.py:66: AssertionError
_______________________________________________________________________ test_empty_permutation _______________________________________________________________________

    def test_empty_permutation():
        """Test input with empty permutation options."""
        result = expand_midjargon_input("a {} bird")
        assert len(result) == 1
>       assert result[0] == "a  bird"
E       AssertionError: assert 'abird' == 'a  bird'
E         
E         - a  bird
E         ?  --
E         + abird

tests/core/test_input.py:81: AssertionError
______________________________________________________________________ test_whitespace_handling ______________________________________________________________________

    def test_whitespace_handling():
        """Test input with various whitespace patterns."""
        result = expand_midjargon_input("a {  red  ,  blue  } bird")
        assert len(result) == PERMUTATION_COUNT_2
>       assert "a red bird" in result
E       AssertionError: assert 'a red bird' in ['a redbird', 'a bluebird']

tests/core/test_input.py:88: AssertionError
_______________________________________________________________________ test_version_parameter _______________________________________________________________________

    def test_version_parameter():
        """Test parsing of version parameter."""
        # Test v parameter
        params = parse_parameters("--v 5.2")
>       assert params["version"] == "5.2"
E       AssertionError: assert 'v5.2' == '5.2'
E         
E         - 5.2
E         + v5.2
E         ? +

tests/core/test_parameters.py:81: AssertionError
______________________________________________________________________ test_invalid_parameters _______________________________________________________________________

    def test_invalid_parameters():
        """Test handling of invalid parameter formats."""
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/core/test_parameters.py:113: Failed
______________________________________________________________________ test_simple_permutation _______________________________________________________________________

    def test_simple_permutation():
        """Test basic permutation expansion."""
        text = "a {red, blue} bird"
        results = expand_text(text)
>       assert set(results) == {"a red bird", "a blue bird"}
E       AssertionError: assert {'a bluebird', 'a redbird'} == {'a blue bird', 'a red bird'}
E         
E         Extra items in the left set:
E         'a bluebird'
E         'a redbird'
E         Extra items in the right set:
E         'a red bird'
E         'a blue bird'...
E         
E         ...Full output truncated (10 lines hidden), use '-vv' to show

tests/core/test_permutations.py:15: AssertionError
_____________________________________________________________________ test_multiple_permutations _____________________________________________________________________

    def test_multiple_permutations():
        """Test handling of multiple permutation groups."""
        text = "a {red, blue} bird on a {flower, leaf}"
        results = expand_text(text)
        expected = {
            "a red bird on a flower",
            "a red bird on a leaf",
            "a blue bird on a flower",
            "a blue bird on a leaf",
        }
>       assert set(results) == expected
E       AssertionError: assert {'a bluebird ...rd on a leaf'} == {'a blue bird...rd on a leaf'}
E         
E         Extra items in the left set:
E         'a bluebird on a flower'
E         'a redbird on a flower'
E         'a redbird on a leaf'
E         'a bluebird on a leaf'
E         Extra items in the right set:...
E         
E         ...Full output truncated (20 lines hidden), use '-vv' to show

tests/core/test_permutations.py:28: AssertionError
______________________________________________________________________ test_nested_permutations ______________________________________________________________________

    def test_nested_permutations():
        """Test handling of nested permutation groups."""
        text = "a {big {red, blue}, small green} bird"
        results = expand_text(text)
        expected = {"a big red bird", "a big blue bird", "a small green bird"}
>       assert set(results) == expected
E       AssertionError: assert {'a big blueb...ll greenbird'} == {'a big blue ...l green bird'}
E         
E         Extra items in the left set:
E         'a big redbird'
E         'a small greenbird'
E         'a big bluebird'
E         Extra items in the right set:
E         'a small green bird'...
E         
E         ...Full output truncated (15 lines hidden), use '-vv' to show

tests/core/test_permutations.py:36: AssertionError
______________________________________________________________________ test_escaped_characters _______________________________________________________________________

    def test_escaped_characters():
        """Test handling of escaped characters in permutations."""
        text = "a {red\\, blue, green} bird"
        results = expand_text(text)
>       assert set(results) == {"a red, blue bird", "a green bird"}
E       AssertionError: assert {'a greenbird...\\, bluebird'} == {'a green bir...d, blue bird'}
E         
E         Extra items in the left set:
E         'a greenbird'
E         'a red\\, bluebird'
E         Extra items in the right set:
E         'a green bird'
E         'a red, blue bird'...
E         
E         ...Full output truncated (11 lines hidden), use '-vv' to show

tests/core/test_permutations.py:43: AssertionError
_________________________________________________________________________ test_empty_options _________________________________________________________________________

    def test_empty_options():
        """Test handling of empty options in permutations."""
        text = "a {, red, } bird"
        results = expand_text(text)
>       assert set(results) == {"a bird", "a red bird"}
E       AssertionError: assert {'a redbird', 'abird'} == {'a bird', 'a red bird'}
E         
E         Extra items in the left set:
E         'abird'
E         'a redbird'
E         Extra items in the right set:
E         'a red bird'
E         'a bird'...
E         
E         ...Full output truncated (9 lines hidden), use '-vv' to show

tests/core/test_permutations.py:50: AssertionError
_________________________________________________________________________ test_single_option _________________________________________________________________________

    def test_single_option():
        """Test handling of single option in permutations."""
        text = "a {red} bird"
        results = expand_text(text)
>       assert set(results) == {"a red bird"}
E       AssertionError: assert {'a redbird'} == {'a red bird'}
E         
E         Extra items in the left set:
E         'a redbird'
E         Extra items in the right set:
E         'a red bird'
E         
E         Full diff:...
E         
E         ...Full output truncated (5 lines hidden), use '-vv' to show

tests/core/test_permutations.py:57: AssertionError
_____________________________________________________________________ test_invalid_permutations ______________________________________________________________________

    def test_invalid_permutations():
        """Test handling of invalid permutation syntax."""
        # Unclosed brace - should be treated as literal
        result = expand_text("a {red, blue bird")
        assert result == ["a {red, blue bird"]
    
        # Unopened brace - should be treated as literal
        result = expand_text("a red} bird")
        assert result == ["a red} bird"]
    
        # Double nested group - should be expanded normally
        result = expand_text("a {{red}} bird")
>       assert result == ["a red bird"]
E       AssertionError: assert ['a redbird'] == ['a red bird']
E         
E         At index 0 diff: 'a redbird' != 'a red bird'
E         
E         Full diff:
E           [
E         -     'a red bird',
E         ?           -
E         +     'a redbird',
E           ]

tests/core/test_permutations.py:84: AssertionError
__________________________________________________________________ test_complex_nested_permutations __________________________________________________________________

    def test_complex_nested_permutations():
        """Test complex nested permutation scenarios."""
        text = "a {big {red, blue} {cat, dog}, small {green, yellow} bird}"
        results = expand_text(text)
        expected = {
            "a big red cat",
            "a big red dog",
            "a big blue cat",
            "a big blue dog",
            "a small green bird",
            "a small yellow bird",
        }
>       assert set(results) == expected
E       AssertionError: assert {'a big blue ...l yellowbird'} == {'a big blue ... yellow bird'}
E         
E         Extra items in the left set:
E         'a small greenbird'
E         'a small yellowbird'
E         Extra items in the right set:
E         'a small yellow bird'
E         'a small green bird'...
E         
E         ...Full output truncated (14 lines hidden), use '-vv' to show

tests/core/test_permutations.py:106: AssertionError
___________________________________________________________________ test_engine_with_empty_prompt ____________________________________________________________________

    def test_engine_with_empty_prompt():
        """Test engine handling of empty prompt."""
        engine = TestEngine()
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/engines/test_base.py:69: Failed
_____________________________________________________________________ test_permutation_workflow ______________________________________________________________________

    def test_permutation_workflow():
        """Test workflow with permutations."""
        prompt = f"a {{red, blue}} bird on a {{branch, rock}} --stylize {STYLIZE_VALUE}"
        results = process_prompt(prompt)
    
        assert len(results) == PERMUTATION_COUNT_2X2  # 2x2 permutations
        texts = {r.text for r in results}
        expected = {
            "a red bird on a branch",
            "a red bird on a rock",
            "a blue bird on a branch",
            "a blue bird on a rock",
        }
>       assert texts == expected
E       AssertionError: assert {'a bluebird ...rd on a rock'} == {'a blue bird...rd on a rock'}
E         
E         Extra items in the left set:
E         'a redbird on a branch'
E         'a bluebird on a branch'
E         'a bluebird on a rock'
E         'a redbird on a rock'
E         Extra items in the right set:...
E         
E         ...Full output truncated (20 lines hidden), use '-vv' to show

tests/integration/test_workflow.py:70: AssertionError
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

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x1102c5550>, midjargon_dict = {'chaos': 50, 'images': [], 'seed': 12345, 'stop': 80, ...}

    def parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """
        Parse a MidjargonDict into a validated MidjourneyPrompt.
    
        Args:
            midjargon_dict: Dictionary from basic parser.
    
        Returns:
            Validated MidjourneyPrompt.
        """
        # Initialize with core components
        images = midjargon_dict.get("images", [])
        if images is None:
            images = []
    
        prompt_data: dict[str, Any] = {
            "text": midjargon_dict["text"],
            "image_prompts": [ImagePrompt(url=url) for url in images],
            "extra_params": {},
            "version": None,
            "personalization": None,
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
    
            # Handle style parameter
            param_name, param_value = self._handle_style_param(name, value)
            if param_name:
                prompt_data[param_name] = param_value
                continue
    
            # Handle version parameter
            param_name, param_value = self._handle_version_param(name, value)
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
    
            # Handle boolean flags
            if name in ("turbo", "relax", "tile"):
                if value is None:
                    prompt_data[name] = True
                else:
                    norm_value = self._normalize_value(value)
                    prompt_data[name] = (
                        norm_value.lower() == "true" if norm_value else False
                    )
                continue
    
            # Store unknown parameters
            prompt_data["extra_params"][name] = value
    
        # Create and validate prompt
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       version
E         Value error, Invalid version value. Must be one of: {'4', '5', '6', '1', '2', '3', '5.1', '5.0', '6.1', '5.2'} [type=value_error, input_value='vniji 6', input_type=str]
E           For further information visit https://errors.pydantic.dev/2.10/v/value_error

src/midjargon/engines/midjourney/parser.py:284: ValidationError
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
        results = process_prompt(prompt)
    
        assert len(results) == 1
        result = results[0]
    
        assert result.text == "portrait photo"
        assert result.quality == QUALITY_VALUE
        assert result.character_weight == CHARACTER_WEIGHT_VALUE
        assert result.style_weight == STYLE_WEIGHT_VALUE
        assert result.style_version == STYLE_VERSION_VALUE
        assert result.repeat == REPEAT_VALUE
>       assert result.character_reference == ["ref1.jpg"]
E       AssertionError: assert [] == ['ref1.jpg']
E         
E         Right contains one more item: 'ref1.jpg'
E         
E         Full diff:
E         + []
E         - [
E         -     'ref1.jpg',
E         - ]

tests/integration/test_workflow.py:140: AssertionError
________________________________________________________________________ test_error_workflow _________________________________________________________________________

    def test_error_workflow():
        """Test error handling in workflow."""
        # Test empty prompt
        with pytest.raises(ValueError, match="Empty prompt"):
            process_prompt("")
    
        # Test invalid parameter value
        with pytest.raises(ValueError):
            process_prompt(f"photo --stylize {STYLIZE_VALUE * 20}")  # Over max
    
        # Test invalid image URL
        with pytest.raises(ValueError):
            process_prompt("http://example.com/image.txt photo")  # Wrong extension
    
        # Test malformed parameters
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/integration/test_workflow.py:170: Failed
========================================================================== warnings summary ==========================================================================
tests/engines/test_base.py:14
  /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/tests/engines/test_base.py:14: PytestCollectionWarning: cannot collect test class 'TestPrompt' because it has a __init__ constructor (from: tests/engines/test_base.py)
    class TestPrompt(BaseModel):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================================================== slowest 10 durations ========================================================================
0.17s call     tests/core/test_permutations.py::test_simple_permutation
0.02s call     tests/cli/test_main.py::test_no_color_output
0.02s call     tests/cli/test_main.py::test_invalid_input
0.01s call     tests/cli/test_main.py::test_image_url_handling

(6 durations < 0.005s hidden.  Use -vv to show these durations.)
====================================================================== short test summary info =======================================================================
FAILED tests/cli/test_main.py::test_basic_prompt - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_permutations - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_raw_output - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_json_output_formatting - AssertionError: assert '\n  ' in ''
FAILED tests/cli/test_main.py::test_invalid_input - AssertionError: assert 'Error' in ''
FAILED tests/cli/test_main.py::test_parameter_validation - AssertionError: assert 'Error' in ''
FAILED tests/cli/test_main.py::test_image_url_handling - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_no_color_output - AssertionError: assert ''
FAILED tests/cli/test_main.py::test_complex_prompt - ValueError: No JSON found in output
FAILED tests/core/test_input.py::test_single_permutation - AssertionError: assert 'a red bird' in ['a redbird', 'a bluebird']
FAILED tests/core/test_input.py::test_empty_input - ValueError: Empty prompt
FAILED tests/core/test_input.py::test_multiple_permutations - AssertionError: assert 'a red bird' in ['a redbird', 'a bluebird', 'a greenbird']
FAILED tests/core/test_input.py::test_escaped_braces - AssertionError: assert 'a {red, blue} bird' == '{red, blue} bird'
FAILED tests/core/test_input.py::test_escaped_commas - AssertionError: assert 'a red, blue bird' in ['a red\\, bluebird', 'a greenbird']
FAILED tests/core/test_input.py::test_empty_permutation - AssertionError: assert 'abird' == 'a  bird'
FAILED tests/core/test_input.py::test_whitespace_handling - AssertionError: assert 'a red bird' in ['a redbird', 'a bluebird']
FAILED tests/core/test_parameters.py::test_version_parameter - AssertionError: assert 'v5.2' == '5.2'
FAILED tests/core/test_parameters.py::test_invalid_parameters - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/core/test_permutations.py::test_simple_permutation - AssertionError: assert {'a bluebird', 'a redbird'} == {'a blue bird', 'a red bird'}
FAILED tests/core/test_permutations.py::test_multiple_permutations - AssertionError: assert {'a bluebird ...rd on a leaf'} == {'a blue bird...rd on a leaf'}
FAILED tests/core/test_permutations.py::test_nested_permutations - AssertionError: assert {'a big blueb...ll greenbird'} == {'a big blue ...l green bird'}
FAILED tests/core/test_permutations.py::test_escaped_characters - AssertionError: assert {'a greenbird...\\, bluebird'} == {'a green bir...d, blue bird'}
FAILED tests/core/test_permutations.py::test_empty_options - AssertionError: assert {'a redbird', 'abird'} == {'a bird', 'a red bird'}
FAILED tests/core/test_permutations.py::test_single_option - AssertionError: assert {'a redbird'} == {'a red bird'}
FAILED tests/core/test_permutations.py::test_invalid_permutations - AssertionError: assert ['a redbird'] == ['a red bird']
FAILED tests/core/test_permutations.py::test_complex_nested_permutations - AssertionError: assert {'a big blue ...l yellowbird'} == {'a big blue ... yellow bird'}
FAILED tests/engines/test_base.py::test_engine_with_empty_prompt - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/integration/test_workflow.py::test_permutation_workflow - AssertionError: assert {'a bluebird ...rd on a rock'} == {'a blue bird...rd on a rock'}
FAILED tests/integration/test_workflow.py::test_parameter_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
FAILED tests/integration/test_workflow.py::test_new_parameters_workflow - AssertionError: assert [] == ['ref1.jpg']
FAILED tests/integration/test_workflow.py::test_error_workflow - Failed: DID NOT RAISE <class 'ValueError'>
============================================================== 31 failed, 35 passed, 1 warning in 1.01s ==============================================================


