================================================================================================ test session starts =================================================================================================
platform darwin -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0 -- /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon
configfile: pytest.ini
testpaths: tests
plugins: cov-6.0.0
collected 66 items                                                                                                                                                                                                   

tests/cli/test_main.py::test_basic_prompt FAILED                                                                                                                                                               [  1%]
tests/cli/test_main.py::test_permutations FAILED                                                                                                                                                               [  3%]
tests/cli/test_main.py::test_raw_output FAILED                                                                                                                                                                 [  4%]
tests/cli/test_main.py::test_json_output_formatting FAILED                                                                                                                                                     [  6%]
tests/cli/test_main.py::test_invalid_input FAILED                                                                                                                                                              [  7%]
tests/cli/test_main.py::test_parameter_validation FAILED                                                                                                                                                       [  9%]
tests/cli/test_main.py::test_image_url_handling FAILED                                                                                                                                                         [ 10%]
tests/cli/test_main.py::test_no_color_output FAILED                                                                                                                                                            [ 12%]
tests/cli/test_main.py::test_complex_prompt FAILED                                                                                                                                                             [ 13%]
tests/core/test_input.py::test_basic_input PASSED                                                                                                                                                              [ 15%]
tests/core/test_input.py::test_single_permutation PASSED                                                                                                                                                       [ 16%]
tests/core/test_input.py::test_empty_input PASSED                                                                                                                                                              [ 18%]
tests/core/test_input.py::test_multiple_permutations PASSED                                                                                                                                                    [ 19%]
tests/core/test_input.py::test_nested_permutations PASSED                                                                                                                                                      [ 21%]
tests/core/test_input.py::test_escaped_braces PASSED                                                                                                                                                           [ 22%]
tests/core/test_input.py::test_escaped_commas PASSED                                                                                                                                                           [ 24%]
tests/core/test_input.py::test_unmatched_braces PASSED                                                                                                                                                         [ 25%]
tests/core/test_input.py::test_empty_permutation PASSED                                                                                                                                                        [ 27%]
tests/core/test_input.py::test_whitespace_handling PASSED                                                                                                                                                      [ 28%]
tests/core/test_parameters.py::test_basic_parameter_parsing PASSED                                                                                                                                             [ 30%]
tests/core/test_parameters.py::test_flag_parameters PASSED                                                                                                                                                     [ 31%]
tests/core/test_parameters.py::test_parameter_with_multiple_values PASSED                                                                                                                                      [ 33%]
tests/core/test_parameters.py::test_parameter_with_spaces PASSED                                                                                                                                               [ 34%]
tests/core/test_parameters.py::test_mixed_parameters PASSED                                                                                                                                                    [ 36%]
tests/core/test_parameters.py::test_shorthand_parameters PASSED                                                                                                                                                [ 37%]
tests/core/test_parameters.py::test_niji_version_parameter PASSED                                                                                                                                              [ 39%]
tests/core/test_parameters.py::test_version_parameter PASSED                                                                                                                                                   [ 40%]
tests/core/test_parameters.py::test_personalization_parameter PASSED                                                                                                                                           [ 42%]
tests/core/test_parameters.py::test_reference_parameters PASSED                                                                                                                                                [ 43%]
tests/core/test_parameters.py::test_parameter_order PASSED                                                                                                                                                     [ 45%]
tests/core/test_parameters.py::test_invalid_parameters FAILED                                                                                                                                                  [ 46%]
tests/core/test_permutations.py::test_simple_permutation PASSED                                                                                                                                                [ 48%]
tests/core/test_permutations.py::test_multiple_permutations PASSED                                                                                                                                             [ 50%]
tests/core/test_permutations.py::test_nested_permutations PASSED                                                                                                                                               [ 51%]
tests/core/test_permutations.py::test_escaped_characters PASSED                                                                                                                                                [ 53%]
tests/core/test_permutations.py::test_empty_options PASSED                                                                                                                                                     [ 54%]
tests/core/test_permutations.py::test_single_option PASSED                                                                                                                                                     [ 56%]
tests/core/test_permutations.py::test_split_permutation_options PASSED                                                                                                                                         [ 57%]
tests/core/test_permutations.py::test_invalid_permutations PASSED                                                                                                                                              [ 59%]
tests/core/test_permutations.py::test_permutations_with_parameters PASSED                                                                                                                                      [ 60%]
tests/core/test_permutations.py::test_complex_nested_permutations PASSED                                                                                                                                       [ 62%]
tests/engines/midjourney/test_parser.py::test_numeric_parameters FAILED                                                                                                                                        [ 63%]
tests/engines/midjourney/test_parser.py::test_style_parameters PASSED                                                                                                                                          [ 65%]
tests/engines/midjourney/test_parser.py::test_aspect_ratio FAILED                                                                                                                                              [ 66%]
tests/engines/midjourney/test_parser.py::test_image_prompts FAILED                                                                                                                                             [ 68%]
tests/engines/midjourney/test_parser.py::test_extra_parameters PASSED                                                                                                                                          [ 69%]
tests/engines/midjourney/test_parser.py::test_parameter_conversion FAILED                                                                                                                                      [ 71%]
tests/engines/midjourney/test_parser.py::test_invalid_values FAILED                                                                                                                                            [ 72%]
tests/engines/midjourney/test_parser.py::test_parameter_ranges FAILED                                                                                                                                          [ 74%]
tests/engines/midjourney/test_parser.py::test_empty_values FAILED                                                                                                                                              [ 75%]
tests/engines/midjourney/test_parser.py::test_niji_parameter PASSED                                                                                                                                            [ 77%]
tests/engines/test_base.py::test_engine_parsing PASSED                                                                                                                                                         [ 78%]
tests/engines/test_base.py::test_prompt_to_string PASSED                                                                                                                                                       [ 80%]
tests/engines/test_base.py::test_engine_validation PASSED                                                                                                                                                      [ 81%]
tests/engines/test_base.py::test_engine_with_empty_prompt PASSED                                                                                                                                               [ 83%]
tests/engines/test_base.py::test_engine_with_complex_prompt PASSED                                                                                                                                             [ 84%]
tests/engines/test_base.py::test_engine_roundtrip PASSED                                                                                                                                                       [ 86%]
tests/integration/test_workflow.py::test_basic_workflow FAILED                                                                                                                                                 [ 87%]
tests/integration/test_workflow.py::test_permutation_workflow FAILED                                                                                                                                           [ 89%]
tests/integration/test_workflow.py::test_image_workflow FAILED                                                                                                                                                 [ 90%]
tests/integration/test_workflow.py::test_parameter_workflow FAILED                                                                                                                                             [ 92%]
tests/integration/test_workflow.py::test_new_parameters_workflow FAILED                                                                                                                                        [ 93%]
tests/integration/test_workflow.py::test_weighted_prompts_workflow FAILED                                                                                                                                      [ 95%]
tests/integration/test_workflow.py::test_error_workflow PASSED                                                                                                                                                 [ 96%]
tests/integration/test_workflow.py::test_complex_workflow FAILED                                                                                                                                               [ 98%]
tests/test_package.py::test_version PASSED                                                                                                                                                                     [100%]/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/.venv/lib/python3.13/site-packages/coverage/inorout.py:508: CoverageWarning: Module tests was never imported. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported")


====================================================================================================== FAILURES ======================================================================================================
_________________________________________________________________________________________________ test_basic_prompt __________________________________________________________________________________________________

prompt = 'a beautiful landscape --ar 16:9'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
>               midjourney = parse_midjourney_dict(parsed)

src/midjargon/cli/main.py:186: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>, midjargon_dict = {'aspect': '16:9', 'images': [], 'text': 'a beautiful landscape'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError

During handling of the above exception, another exception occurred:

    def test_basic_prompt():
        """Test basic prompt processing."""
        with StringIO() as capture_stdout:
            sys.stdout = capture_stdout
>           main(
                f"a beautiful landscape --ar {ASPECT_WIDTH}:{ASPECT_HEIGHT}",
                json_output=True,
            )

tests/cli/test_main.py:51: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

prompt = 'a beautiful landscape --ar 16:9'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
                midjourney = parse_midjourney_dict(parsed)
                results.append(midjourney)
    
            if json_output:
                if raw:
                    _output_json(results)
                else:
                    # Convert Pydantic models to dicts for JSON serialization
                    json_results = [prompt.model_dump() for prompt in results]
                    _output_json(json_results)
                sys.stdout.flush()
                import time
    
                time.sleep(0.05)
                return
    
            # Display results
            for i, result in enumerate(results, 1):
                if len(results) > 1:
                    console.print(f"\nVariant {i}:", style="bold blue")
                if raw:
                    console.print(Panel(str(result)))
                else:
                    console.print(Panel(format_prompt(result)))
    
        except Exception as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.stdout.flush()
>               sys.exit(1)
E               SystemExit: 1

src/midjargon/cli/main.py:215: SystemExit
_________________________________________________________________________________________________ test_permutations __________________________________________________________________________________________________

prompt = 'a {red, blue} bird'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
>               midjourney = parse_midjourney_dict(parsed)

src/midjargon/cli/main.py:186: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>, midjargon_dict = {'images': [], 'text': 'a red bird'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError

During handling of the above exception, another exception occurred:

    def test_permutations():
        """Test permutation processing."""
        with StringIO() as capture_stdout:
            sys.stdout = capture_stdout
>           main("a {red, blue} bird", json_output=True)

tests/cli/test_main.py:69: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

prompt = 'a {red, blue} bird'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
                midjourney = parse_midjourney_dict(parsed)
                results.append(midjourney)
    
            if json_output:
                if raw:
                    _output_json(results)
                else:
                    # Convert Pydantic models to dicts for JSON serialization
                    json_results = [prompt.model_dump() for prompt in results]
                    _output_json(json_results)
                sys.stdout.flush()
                import time
    
                time.sleep(0.05)
                return
    
            # Display results
            for i, result in enumerate(results, 1):
                if len(results) > 1:
                    console.print(f"\nVariant {i}:", style="bold blue")
                if raw:
                    console.print(Panel(str(result)))
                else:
                    console.print(Panel(format_prompt(result)))
    
        except Exception as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.stdout.flush()
>               sys.exit(1)
E               SystemExit: 1

src/midjargon/cli/main.py:215: SystemExit
__________________________________________________________________________________________________ test_raw_output ___________________________________________________________________________________________________

    def test_raw_output():
        """Test raw output mode."""
        with StringIO() as capture_stdout:
            sys.stdout = capture_stdout
            main(f"a photo --stylize {STYLIZE_VALUE}", raw=True, json_output=True)
            sys.stdout = sys.__stdout__
>           data = parse_json_output(capture_stdout)

tests/cli/test_main.py:84: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output_stream = <_io.StringIO object at 0x105bd0640>

    def parse_json_output(output_stream: StringIO) -> Any:
        """Parse JSON output from the CLI, removing ANSI escape sequences if any."""
        output_stream.seek(0)
        output = output_stream.getvalue()
        # Remove ANSI escape sequences
        output = ANSI_ESCAPE.sub("", output)
        output = output.strip()
        if not output:
            msg = "No JSON found in output"
>           raise ValueError(msg)
E           ValueError: No JSON found in output

tests/cli/test_main.py:39: ValueError
____________________________________________________________________________________________ test_json_output_formatting _____________________________________________________________________________________________

prompt = 'a photo'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
>               midjourney = parse_midjourney_dict(parsed)

src/midjargon/cli/main.py:186: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>, midjargon_dict = {'images': [], 'text': 'a photo'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError

During handling of the above exception, another exception occurred:

    def test_json_output_formatting():
        """Test JSON output formatting."""
        with StringIO() as capture_stdout:
            sys.stdout = capture_stdout
>           main("a photo", json_output=True)

tests/cli/test_main.py:96: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

prompt = 'a photo'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
                midjourney = parse_midjourney_dict(parsed)
                results.append(midjourney)
    
            if json_output:
                if raw:
                    _output_json(results)
                else:
                    # Convert Pydantic models to dicts for JSON serialization
                    json_results = [prompt.model_dump() for prompt in results]
                    _output_json(json_results)
                sys.stdout.flush()
                import time
    
                time.sleep(0.05)
                return
    
            # Display results
            for i, result in enumerate(results, 1):
                if len(results) > 1:
                    console.print(f"\nVariant {i}:", style="bold blue")
                if raw:
                    console.print(Panel(str(result)))
                else:
                    console.print(Panel(format_prompt(result)))
    
        except Exception as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.stdout.flush()
>               sys.exit(1)
E               SystemExit: 1

src/midjargon/cli/main.py:215: SystemExit
_________________________________________________________________________________________________ test_invalid_input _________________________________________________________________________________________________

    def test_invalid_input():
        """Test handling of invalid input."""
        with StringIO() as capture_stdout:
            with pytest.raises(SystemExit):
                sys.stdout = capture_stdout
                main("", json_output=True)
            sys.stdout = sys.__stdout__
>           data = parse_json_output(capture_stdout)

tests/cli/test_main.py:110: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output_stream = <_io.StringIO object at 0x105bd0c40>

    def parse_json_output(output_stream: StringIO) -> Any:
        """Parse JSON output from the CLI, removing ANSI escape sequences if any."""
        output_stream.seek(0)
        output = output_stream.getvalue()
        # Remove ANSI escape sequences
        output = ANSI_ESCAPE.sub("", output)
        output = output.strip()
        if not output:
            msg = "No JSON found in output"
>           raise ValueError(msg)
E           ValueError: No JSON found in output

tests/cli/test_main.py:39: ValueError
_____________________________________________________________________________________________ test_parameter_validation ______________________________________________________________________________________________

    def test_parameter_validation():
        """Test parameter validation."""
        with StringIO() as capture_stdout:
            with pytest.raises(SystemExit):
                sys.stdout = capture_stdout
                main(
                    f"a photo --stylize {STYLIZE_VALUE * 20}", json_output=True
                )  # Over max
            sys.stdout = sys.__stdout__
>           data = parse_json_output(capture_stdout)

tests/cli/test_main.py:123: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

output_stream = <_io.StringIO object at 0x105bd1240>

    def parse_json_output(output_stream: StringIO) -> Any:
        """Parse JSON output from the CLI, removing ANSI escape sequences if any."""
        output_stream.seek(0)
        output = output_stream.getvalue()
        # Remove ANSI escape sequences
        output = ANSI_ESCAPE.sub("", output)
        output = output.strip()
        if not output:
            msg = "No JSON found in output"
>           raise ValueError(msg)
E           ValueError: No JSON found in output

tests/cli/test_main.py:39: ValueError
______________________________________________________________________________________________ test_image_url_handling _______________________________________________________________________________________________

prompt = 'https://example.com/image.jpg a fusion'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
>               midjourney = parse_midjourney_dict(parsed)

src/midjargon/cli/main.py:186: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>, midjargon_dict = {'images': ['https://example.com/image.jpg'], 'text': 'a fusion'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=['https://example.com/image.jpg'], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError

During handling of the above exception, another exception occurred:

    def test_image_url_handling():
        """Test handling of image URLs."""
        url = "https://example.com/image.jpg"
        with StringIO() as capture_stdout:
            sys.stdout = capture_stdout
>           main(f"{url} a fusion", json_output=True)

tests/cli/test_main.py:132: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

prompt = 'https://example.com/image.jpg a fusion'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
                midjourney = parse_midjourney_dict(parsed)
                results.append(midjourney)
    
            if json_output:
                if raw:
                    _output_json(results)
                else:
                    # Convert Pydantic models to dicts for JSON serialization
                    json_results = [prompt.model_dump() for prompt in results]
                    _output_json(json_results)
                sys.stdout.flush()
                import time
    
                time.sleep(0.05)
                return
    
            # Display results
            for i, result in enumerate(results, 1):
                if len(results) > 1:
                    console.print(f"\nVariant {i}:", style="bold blue")
                if raw:
                    console.print(Panel(str(result)))
                else:
                    console.print(Panel(format_prompt(result)))
    
        except Exception as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.stdout.flush()
>               sys.exit(1)
E               SystemExit: 1

src/midjargon/cli/main.py:215: SystemExit
________________________________________________________________________________________________ test_no_color_output ________________________________________________________________________________________________

prompt = 'a photo'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
>               midjourney = parse_midjourney_dict(parsed)

src/midjargon/cli/main.py:186: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>, midjargon_dict = {'images': [], 'text': 'a photo'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError

During handling of the above exception, another exception occurred:

    def test_no_color_output():
        """Test no-color output mode."""
        Console(force_terminal=False)
        with StringIO() as capture_stdout:
            sys.stdout = capture_stdout
>           main("a photo", json_output=True)

tests/cli/test_main.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

prompt = 'a photo'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
                midjourney = parse_midjourney_dict(parsed)
                results.append(midjourney)
    
            if json_output:
                if raw:
                    _output_json(results)
                else:
                    # Convert Pydantic models to dicts for JSON serialization
                    json_results = [prompt.model_dump() for prompt in results]
                    _output_json(json_results)
                sys.stdout.flush()
                import time
    
                time.sleep(0.05)
                return
    
            # Display results
            for i, result in enumerate(results, 1):
                if len(results) > 1:
                    console.print(f"\nVariant {i}:", style="bold blue")
                if raw:
                    console.print(Panel(str(result)))
                else:
                    console.print(Panel(format_prompt(result)))
    
        except Exception as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.stdout.flush()
>               sys.exit(1)
E               SystemExit: 1

src/midjargon/cli/main.py:215: SystemExit
________________________________________________________________________________________________ test_complex_prompt _________________________________________________________________________________________________

prompt = 'https://example.com/img1.jpg https://example.com/img2.jpg a {red, blue} bird on a {branch, rock} --ar 16:9 --stylize 100 --chaos 50'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
>               midjourney = parse_midjourney_dict(parsed)

src/midjargon/cli/main.py:186: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>
midjargon_dict = {'aspect': '16:9', 'chaos': 50, 'images': ['https://example.com/img1.jpg', 'https://example.com/img2.jpg'], 'stylize': 100, ...}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=['https://example.com/img...//example.com/img2.jpg'], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError

During handling of the above exception, another exception occurred:

    def test_complex_prompt():
        """Test complex prompt with multiple features."""
        prompt = (
            "https://example.com/img1.jpg https://example.com/img2.jpg "
            "a {red, blue} bird on a {branch, rock} "
            f"--ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE} --chaos {CHAOS_VALUE}"
        )
        with StringIO() as capture_stdout:
            sys.stdout = capture_stdout
>           main(prompt, json_output=True)

tests/cli/test_main.py:164: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

prompt = 'https://example.com/img1.jpg https://example.com/img2.jpg a {red, blue} bird on a {branch, rock} --ar 16:9 --stylize 100 --chaos 50'

    def main(
        prompt: str,
        *,  # Make all following arguments keyword-only
        raw: bool = False,
        json_output: bool = False,  # -j is an alias for --json_output
        no_color: bool = False,
    ) -> None:
        """
        Parse and validate a Midjourney prompt.
    
        Args:
            prompt: The Midjourney prompt string to parse.
            raw: If True, show the raw parsed structure before validation.
            json_output: If True, output in JSON format (alias: -j).
            no_color: If True, disable colored output.
    
        Example prompts:
            "A portrait of a wise old man --style raw --v 5.1"
            "https://example.com/image1.jpg https://example.com/image2.jpg abstract fusion"
            "A {red, blue, green} bird on a {branch, rock} --ar 16:9"
            "futuristic city::2 cyberpunk aesthetic::1 --stylize 100"
            "elephant {, --s {200, 300}}"
        """
        console = Console(force_terminal=not no_color)
    
        try:
            # Expand permutations
            expanded = expand_midjargon_input(prompt)
    
            # Process each expanded prompt
            results = []
            for exp_prompt in expanded:
                # Parse into dictionary
                parsed = parse_midjargon_prompt_to_dict(exp_prompt)
                if raw:
                    results.append(parsed)
                    continue
    
                # Parse for Midjourney
                midjourney = parse_midjourney_dict(parsed)
                results.append(midjourney)
    
            if json_output:
                if raw:
                    _output_json(results)
                else:
                    # Convert Pydantic models to dicts for JSON serialization
                    json_results = [prompt.model_dump() for prompt in results]
                    _output_json(json_results)
                sys.stdout.flush()
                import time
    
                time.sleep(0.05)
                return
    
            # Display results
            for i, result in enumerate(results, 1):
                if len(results) > 1:
                    console.print(f"\nVariant {i}:", style="bold blue")
                if raw:
                    console.print(Panel(str(result)))
                else:
                    console.print(Panel(format_prompt(result)))
    
        except Exception as error:
            if json_output:
                _output_json({"error": str(error)})
                sys.stdout.flush()
>               sys.exit(1)
E               SystemExit: 1

src/midjargon/cli/main.py:215: SystemExit
______________________________________________________________________________________________ test_invalid_parameters _______________________________________________________________________________________________

    def test_invalid_parameters():
        """Test handling of invalid parameter formats."""
        with pytest.raises(ValueError):
            parse_parameters("--")  # Empty parameter name
    
        with pytest.raises(ValueError):
            parse_parameters("--ar")  # Missing required value
    
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/core/test_parameters.py:123: Failed
______________________________________________________________________________________________ test_numeric_parameters _______________________________________________________________________________________________

    def test_numeric_parameters():
        """Test parsing of numeric parameters."""
        parser = MidjourneyParser()
        prompt = parser.parse_dict(
            {
                "text": "a photo",
                "stylize": str(STYLIZE_VALUE),
                "seed": str(SEED_VALUE),
                "chaos": str(CHAOS_VALUE),
            }
        )
    
        assert prompt.text == "a photo"
        assert prompt.stylize == STYLIZE_VALUE
>       assert prompt.seed == SEED_VALUE
E       AssertionError: assert None == 12345
E        +  where None = MidjourneyPrompt(text='a photo', image_prompts=[], stylize=100, chaos=50, weird=None, image_weight=None, seed=None, stop=None, aspect_width=None, aspect_height=None, style=None, version=None, personalization=None, quality=None, character_reference=[], character_weight=None, style_reference=[], style_weight=None, style_version=None, repeat=None, turbo=False, relax=False, tile=False, negative_prompt=None, extra_params={}).seed

tests/engines/midjourney/test_parser.py:36: AssertionError
_________________________________________________________________________________________________ test_aspect_ratio __________________________________________________________________________________________________

    def test_aspect_ratio():
        """Test parsing of aspect ratio."""
        parser = MidjourneyParser()
        prompt = parser.parse_dict({"text": "a photo", "aspect": "16:9"})
    
        assert prompt.text == "a photo"
>       assert prompt.aspect_width == 16
E       AssertionError: assert None == 16
E        +  where None = MidjourneyPrompt(text='a photo', image_prompts=[], stylize=None, chaos=None, weird=None, image_weight=None, seed=None, stop=None, aspect_width=None, aspect_height=None, style=None, version=None, personalization=None, quality=None, character_reference=[], character_weight=None, style_reference=[], style_weight=None, style_version=None, repeat=None, turbo=False, relax=False, tile=False, negative_prompt=None, extra_params={'aspect': '16:9'}).aspect_width

tests/engines/midjourney/test_parser.py:56: AssertionError
_________________________________________________________________________________________________ test_image_prompts _________________________________________________________________________________________________

    def test_image_prompts():
        """Test parsing of image prompts."""
        parser = MidjourneyParser()
        urls = [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg",
        ]
>       prompt = parser.parse_dict({"text": "a fusion", "images": urls})

tests/engines/midjourney/test_parser.py:67: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105b49a70>, midjargon_dict = {'images': ['https://example.com/image1.jpg', 'https://example.com/image2.jpg'], 'text': 'a fusion'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=['https://example.com/ima...example.com/image2.jpg'], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError
_____________________________________________________________________________________________ test_parameter_conversion ______________________________________________________________________________________________

    def test_parameter_conversion():
        """Test parameter value conversion."""
        parser = MidjourneyParser()
        prompt = parser.parse_dict(
            {
                "text": "a photo",
                "stylize": str(STYLIZE_VALUE),
                "seed": str(SEED_VALUE),
                "iw": str(IMAGE_WEIGHT_VALUE),
            }
        )
    
        assert prompt.text == "a photo"
        assert prompt.stylize == STYLIZE_VALUE
>       assert prompt.seed == SEED_VALUE
E       AssertionError: assert None == 12345
E        +  where None = MidjourneyPrompt(text='a photo', image_prompts=[], stylize=100, chaos=None, weird=None, image_weight=2.0, seed=None, stop=None, aspect_width=None, aspect_height=None, style=None, version=None, personalization=None, quality=None, character_reference=[], character_weight=None, style_reference=[], style_weight=None, style_version=None, repeat=None, turbo=False, relax=False, tile=False, negative_prompt=None, extra_params={'iw': '2.0'}).seed

tests/engines/midjourney/test_parser.py:103: AssertionError
________________________________________________________________________________________________ test_invalid_values _________________________________________________________________________________________________

    def test_invalid_values():
        """Test handling of invalid parameter values."""
        parser = MidjourneyParser()
    
        # Invalid aspect ratio
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/engines/midjourney/test_parser.py:112: Failed
_______________________________________________________________________________________________ test_parameter_ranges ________________________________________________________________________________________________

    def test_parameter_ranges():
        """Test parameter value range validation."""
        parser = MidjourneyParser()
    
        # Test maximum values
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/engines/midjourney/test_parser.py:134: Failed
_________________________________________________________________________________________________ test_empty_values __________________________________________________________________________________________________

    def test_empty_values():
        """Test handling of empty values."""
        parser = MidjourneyParser()
    
        # Empty text
        with pytest.raises(ValueError):
            parser.parse_dict({"text": ""})
    
        # Empty image list
>       prompt = parser.parse_dict({"text": "a photo", "images": []})

tests/engines/midjourney/test_parser.py:151: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105bde250>, midjargon_dict = {'images': [], 'text': 'a photo'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError
________________________________________________________________________________________________ test_basic_workflow _________________________________________________________________________________________________

    def test_basic_workflow():
        """Test basic prompt workflow without permutations."""
        prompt = f"a beautiful landscape --ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE}"
>       results = process_prompt(prompt)

tests/integration/test_workflow.py:46: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/integration/test_workflow.py:40: in process_prompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>, midjargon_dict = {'aspect': '16:9', 'images': [], 'stylize': 100, 'text': 'a beautiful landscape'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError
_____________________________________________________________________________________________ test_permutation_workflow ______________________________________________________________________________________________

    def test_permutation_workflow():
        """Test workflow with permutations."""
        prompt = f"a {{red, blue}} bird on a {{branch, rock}} --stylize {STYLIZE_VALUE}"
>       results = process_prompt(prompt)

tests/integration/test_workflow.py:60: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/integration/test_workflow.py:40: in process_prompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>, midjargon_dict = {'images': [], 'stylize': 100, 'text': 'a red bird on a branch'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError
________________________________________________________________________________________________ test_image_workflow _________________________________________________________________________________________________

    def test_image_workflow():
        """Test workflow with image URLs."""
        urls = [
            "https://example.com/image1.jpg",
            "https://example.com/image2.jpg",
        ]
        prompt = f"{' '.join(urls)} abstract fusion --iw {IMAGE_WEIGHT_VALUE}"
>       results = process_prompt(prompt)

tests/integration/test_workflow.py:81: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/integration/test_workflow.py:40: in process_prompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>
midjargon_dict = {'image_weight': 2.0, 'images': ['https://example.com/image1.jpg', 'https://example.com/image2.jpg'], 'text': 'abstract fusion'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=['https://example.com/ima...example.com/image2.jpg'], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError
______________________________________________________________________________________________ test_parameter_workflow _______________________________________________________________________________________________

    def test_parameter_workflow():
        """Test workflow with various parameter types."""
        prompt = (
            "cyberpunk city --v 5.2 --style raw "
            f"--chaos {CHAOS_VALUE} --weird {WEIRD_VALUE} "
            f"--seed {SEED_VALUE} --stop {STOP_VALUE} "
            "--turbo --tile"
        )
>       results = process_prompt(prompt)

tests/integration/test_workflow.py:100: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/integration/test_workflow.py:40: in process_prompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>, midjargon_dict = {'chaos': 50, 'images': [], 'seed': 12345, 'stop': 80, ...}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError
____________________________________________________________________________________________ test_new_parameters_workflow ____________________________________________________________________________________________

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
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/integration/test_workflow.py:40: in process_prompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>
midjargon_dict = {'character_reference': 'ref1.jpg', 'character_weight': 100, 'images': [], 'personalization': 'custom_profile', ...}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError
___________________________________________________________________________________________ test_weighted_prompts_workflow ___________________________________________________________________________________________

    def test_weighted_prompts_workflow():
        """Test workflow with weighted prompts."""
        prompt = "cyberpunk city::2 neon lights::1"
>       results = process_prompt(prompt)

tests/integration/test_workflow.py:148: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/integration/test_workflow.py:40: in process_prompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>, midjargon_dict = {'images': [], 'text': 'cyberpunk city::2 neon lights::1'}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=[], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError
_______________________________________________________________________________________________ test_complex_workflow ________________________________________________________________________________________________

    def test_complex_workflow():
        """Test workflow with multiple features combined."""
        prompt = (
            "https://example.com/img1.jpg https://example.com/img2.jpg "
            "a {vintage, modern} {portrait, landscape} "
            "with {warm, cool} tones "
            f"--ar {ASPECT_WIDTH}:{ASPECT_HEIGHT} --stylize {STYLIZE_VALUE} "
            f"--chaos {CHAOS_VALUE} --v 5.2 --style raw "
            f"--quality {QUALITY_VALUE} --cw {CHARACTER_WEIGHT_VALUE} "
            "--turbo"
        )
>       results = process_prompt(prompt)

tests/integration/test_workflow.py:197: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
tests/integration/test_workflow.py:40: in process_prompt
    return [parse_midjourney_dict(d) for d in midjargon_dicts]
src/midjargon/engines/midjourney/parser.py:1222: in parse_dict
    super().parse_dict(midjargon_dict)
src/midjargon/engines/base.py:71: in parse_dict
    return self._parse_dict(midjargon_dict)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <midjargon.engines.midjourney.parser.MidjourneyParser object at 0x105326900>
midjargon_dict = {'aspect': '16:9', 'chaos': 50, 'character_weight': 100, 'images': ['https://example.com/img1.jpg', 'https://example.com/img2.jpg'], ...}

    def _parse_dict(self, midjargon_dict: MidjargonDict) -> MidjourneyPrompt:
        """Parse a dictionary into a MidjourneyPrompt."""
        prompt_data = self._get_default_prompt_data()
    
        # Process text and images first
        self._process_text_and_images(prompt_data, midjargon_dict)
    
        # Process version parameters first to ensure correct precedence
        self._process_version_params(prompt_data, midjargon_dict)
    
        # Process other parameter types
        self._process_numeric_params(prompt_data, midjargon_dict)
        self._process_style_params(prompt_data, midjargon_dict)
        self._process_aspect_ratio(prompt_data, midjargon_dict)
        self._process_reference_params(prompt_data, midjargon_dict)
        self._process_flag_params(prompt_data, midjargon_dict)
        self._process_extra_params(prompt_data, midjargon_dict)
    
>       return MidjourneyPrompt(**prompt_data)
E       pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
E       extra_params.images
E         Input should be a valid string [type=string_type, input_value=['https://example.com/img...//example.com/img2.jpg'], input_type=list]
E           For further information visit https://errors.pydantic.dev/2.10/v/string_type

src/midjargon/engines/midjourney/parser.py:1206: ValidationError
================================================================================================== warnings summary ==================================================================================================
tests/engines/test_base.py:14
  /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/tests/engines/test_base.py:14: PytestCollectionWarning: cannot collect test class 'TestPrompt' because it has a __init__ constructor (from: tests/engines/test_base.py)
    class TestPrompt(BaseModel):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================================================ slowest 10 durations ================================================================================================
0.05s call     tests/cli/test_main.py::test_raw_output
0.01s teardown tests/cli/test_main.py::test_image_url_handling
0.00s call     tests/cli/test_main.py::test_image_url_handling
0.00s call     tests/integration/test_workflow.py::test_complex_workflow
0.00s call     tests/integration/test_workflow.py::test_error_workflow
0.00s call     tests/engines/midjourney/test_parser.py::test_numeric_parameters
0.00s setup    tests/engines/midjourney/test_parser.py::test_numeric_parameters
0.00s call     tests/engines/midjourney/test_parser.py::test_parameter_conversion
0.00s call     tests/cli/test_main.py::test_complex_prompt
0.00s call     tests/cli/test_main.py::test_basic_prompt
============================================================================================== short test summary info ===============================================================================================
FAILED tests/cli/test_main.py::test_basic_prompt - SystemExit: 1
FAILED tests/cli/test_main.py::test_permutations - SystemExit: 1
FAILED tests/cli/test_main.py::test_raw_output - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_json_output_formatting - SystemExit: 1
FAILED tests/cli/test_main.py::test_invalid_input - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_parameter_validation - ValueError: No JSON found in output
FAILED tests/cli/test_main.py::test_image_url_handling - SystemExit: 1
FAILED tests/cli/test_main.py::test_no_color_output - SystemExit: 1
FAILED tests/cli/test_main.py::test_complex_prompt - SystemExit: 1
FAILED tests/core/test_parameters.py::test_invalid_parameters - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/engines/midjourney/test_parser.py::test_numeric_parameters - AssertionError: assert None == 12345
 +  where None = MidjourneyPrompt(text='a photo', image_prompts=[], stylize=100, chaos=50, weird=None, image_weight=None, seed=None, stop=None, aspect_width=None, aspect_height=None, style=None, version=None, personalization=None, quality=None, character_reference=[], character_weight=None, style_reference=[], style_weight=None, style_version=None, repeat=None, turbo=False, relax=False, tile=False, negative_prompt=None, extra_params={}).seed
FAILED tests/engines/midjourney/test_parser.py::test_aspect_ratio - AssertionError: assert None == 16
 +  where None = MidjourneyPrompt(text='a photo', image_prompts=[], stylize=None, chaos=None, weird=None, image_weight=None, seed=None, stop=None, aspect_width=None, aspect_height=None, style=None, version=None, personalization=None, quality=None, character_reference=[], character_weight=None, style_reference=[], style_weight=None, style_version=None, repeat=None, turbo=False, relax=False, tile=False, negative_prompt=None, extra_params={'aspect': '16:9'}).aspect_width
FAILED tests/engines/midjourney/test_parser.py::test_image_prompts - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
extra_params.images
  Input should be a valid string [type=string_type, input_value=['https://example.com/ima...example.com/image2.jpg'], input_type=list]
    For further information visit https://errors.pydantic.dev/2.10/v/string_type
FAILED tests/engines/midjourney/test_parser.py::test_parameter_conversion - AssertionError: assert None == 12345
 +  where None = MidjourneyPrompt(text='a photo', image_prompts=[], stylize=100, chaos=None, weird=None, image_weight=2.0, seed=None, stop=None, aspect_width=None, aspect_height=None, style=None, version=None, personalization=None, quality=None, character_reference=[], character_weight=None, style_reference=[], style_weight=None, style_version=None, repeat=None, turbo=False, relax=False, tile=False, negative_prompt=None, extra_params={'iw': '2.0'}).seed
FAILED tests/engines/midjourney/test_parser.py::test_invalid_values - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/engines/midjourney/test_parser.py::test_parameter_ranges - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/engines/midjourney/test_parser.py::test_empty_values - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
extra_params.images
  Input should be a valid string [type=string_type, input_value=[], input_type=list]
    For further information visit https://errors.pydantic.dev/2.10/v/string_type
FAILED tests/integration/test_workflow.py::test_basic_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
extra_params.images
  Input should be a valid string [type=string_type, input_value=[], input_type=list]
    For further information visit https://errors.pydantic.dev/2.10/v/string_type
FAILED tests/integration/test_workflow.py::test_permutation_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
extra_params.images
  Input should be a valid string [type=string_type, input_value=[], input_type=list]
    For further information visit https://errors.pydantic.dev/2.10/v/string_type
FAILED tests/integration/test_workflow.py::test_image_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
extra_params.images
  Input should be a valid string [type=string_type, input_value=['https://example.com/ima...example.com/image2.jpg'], input_type=list]
    For further information visit https://errors.pydantic.dev/2.10/v/string_type
FAILED tests/integration/test_workflow.py::test_parameter_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
extra_params.images
  Input should be a valid string [type=string_type, input_value=[], input_type=list]
    For further information visit https://errors.pydantic.dev/2.10/v/string_type
FAILED tests/integration/test_workflow.py::test_new_parameters_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
extra_params.images
  Input should be a valid string [type=string_type, input_value=[], input_type=list]
    For further information visit https://errors.pydantic.dev/2.10/v/string_type
FAILED tests/integration/test_workflow.py::test_weighted_prompts_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
extra_params.images
  Input should be a valid string [type=string_type, input_value=[], input_type=list]
    For further information visit https://errors.pydantic.dev/2.10/v/string_type
FAILED tests/integration/test_workflow.py::test_complex_workflow - pydantic_core._pydantic_core.ValidationError: 1 validation error for MidjourneyPrompt
extra_params.images
  Input should be a valid string [type=string_type, input_value=['https://example.com/img...//example.com/img2.jpg'], input_type=list]
    For further information visit https://errors.pydantic.dev/2.10/v/string_type
====================================================================================== 24 failed, 42 passed, 1 warning in 2.35s ======================================================================================