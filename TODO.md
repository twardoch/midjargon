Fix the test failures, after each fix, run the tests to ensure that the issue is fixed. Then remove that task from the text in @TODO.md 

================================================================================================ test session starts =================================================================================================
platform darwin -- Python 3.13.1, pytest-8.3.4, pluggy-1.5.0 -- /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon
configfile: pytest.ini
testpaths: tests
plugins: cov-6.0.0
collected 66 items                                                                                                                                                                                                   

tests/cli/test_main.py::test_basic_prompt PASSED                                                                                                                                                               [  1%]
tests/cli/test_main.py::test_permutations PASSED                                                                                                                                                               [  3%]
tests/cli/test_main.py::test_raw_output PASSED                                                                                                                                                                 [  4%]
tests/cli/test_main.py::test_json_output_formatting PASSED                                                                                                                                                     [  6%]
tests/cli/test_main.py::test_invalid_input PASSED                                                                                                                                                              [  7%]
tests/cli/test_main.py::test_parameter_validation PASSED                                                                                                                                                       [  9%]
tests/cli/test_main.py::test_image_url_handling PASSED                                                                                                                                                         [ 10%]
tests/cli/test_main.py::test_no_color_output PASSED                                                                                                                                                            [ 12%]
tests/cli/test_main.py::test_complex_prompt PASSED                                                                                                                                                             [ 13%]
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
tests/engines/midjourney/test_parser.py::test_numeric_parameters PASSED                                                                                                                                        [ 63%]
tests/engines/midjourney/test_parser.py::test_style_parameters PASSED                                                                                                                                          [ 65%]
tests/engines/midjourney/test_parser.py::test_aspect_ratio PASSED                                                                                                                                              [ 66%]
tests/engines/midjourney/test_parser.py::test_image_prompts PASSED                                                                                                                                             [ 68%]
tests/engines/midjourney/test_parser.py::test_extra_parameters FAILED                                                                                                                                          [ 69%]
tests/engines/midjourney/test_parser.py::test_parameter_conversion PASSED                                                                                                                                      [ 71%]
tests/engines/midjourney/test_parser.py::test_invalid_values PASSED                                                                                                                                            [ 72%]
tests/engines/midjourney/test_parser.py::test_parameter_ranges PASSED                                                                                                                                          [ 74%]
tests/engines/midjourney/test_parser.py::test_empty_values PASSED                                                                                                                                              [ 75%]
tests/engines/midjourney/test_parser.py::test_niji_parameter PASSED                                                                                                                                            [ 77%]
tests/engines/test_base.py::test_engine_parsing PASSED                                                                                                                                                         [ 78%]
tests/engines/test_base.py::test_prompt_to_string PASSED                                                                                                                                                       [ 80%]
tests/engines/test_base.py::test_engine_validation PASSED                                                                                                                                                      [ 81%]
tests/engines/test_base.py::test_engine_with_empty_prompt FAILED                                                                                                                                               [ 83%]
tests/engines/test_base.py::test_engine_with_complex_prompt PASSED                                                                                                                                             [ 84%]
tests/engines/test_base.py::test_engine_roundtrip PASSED                                                                                                                                                       [ 86%]
tests/integration/test_workflow.py::test_basic_workflow PASSED                                                                                                                                                 [ 87%]
tests/integration/test_workflow.py::test_permutation_workflow PASSED                                                                                                                                           [ 89%]
tests/integration/test_workflow.py::test_image_workflow PASSED                                                                                                                                                 [ 90%]
tests/integration/test_workflow.py::test_parameter_workflow FAILED                                                                                                                                             [ 92%]
tests/integration/test_workflow.py::test_new_parameters_workflow PASSED                                                                                                                                        [ 93%]
tests/integration/test_workflow.py::test_weighted_prompts_workflow PASSED                                                                                                                                      [ 95%]
tests/integration/test_workflow.py::test_error_workflow FAILED                                                                                                                                                 [ 96%]
tests/integration/test_workflow.py::test_complex_workflow FAILED                                                                                                                                               [ 98%]
tests/test_package.py::test_version PASSED                                                                                                                                                                     [100%]/Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/.venv/lib/python3.13/site-packages/coverage/inorout.py:508: CoverageWarning: Module tests was never imported. (module-not-imported)
  self.warn(f"Module {pkg} was never imported.", slug="module-not-imported")


====================================================================================================== FAILURES ======================================================================================================
______________________________________________________________________________________________ test_invalid_parameters _______________________________________________________________________________________________

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
_______________________________________________________________________________________________ test_extra_parameters ________________________________________________________________________________________________

    def test_extra_parameters():
        """Test handling of unknown parameters."""
        parser = MidjourneyParser()
        prompt = parser.parse_dict(
            {
                "text": "a photo",
                "unknown": "value",
                "flag": None,
            }
        )
    
        assert prompt.text == "a photo"
>       assert prompt.extra_params == {"unknown": "value", "flag": None}
E       AssertionError: assert {'flag': None} == {'unknown': 'value', 'flag': None}
E         
E         Common items:
E         {'flag': None}
E         Right contains 1 more item:
E         {'unknown': 'value'}
E         
E         Full diff:
E           {
E               'flag': None,
E         -     'unknown': 'value',
E           }

tests/engines/midjourney/test_parser.py:86: AssertionError
___________________________________________________________________________________________ test_engine_with_empty_prompt ____________________________________________________________________________________________

    def test_engine_with_empty_prompt():
        """Test engine handling of empty prompt."""
        engine = TestEngine()
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/engines/test_base.py:69: Failed
______________________________________________________________________________________________ test_parameter_workflow _______________________________________________________________________________________________

    def test_parameter_workflow():
        """Test workflow with various parameter types."""
        prompt = (
            "cyberpunk city --v 5.2 --style raw --niji 6 "
            f"--chaos {CHAOS_VALUE} --weird {WEIRD_VALUE} "
            f"--seed {SEED_VALUE} --stop {STOP_VALUE} "
            "--turbo --tile"
        )
        results = process_prompt(prompt)
    
        assert len(results) == 1
        result = results[0]
    
        assert result.text == "cyberpunk city"
>       assert result.version == "v5.2"
E       AssertionError: assert 'niji 6' == 'v5.2'
E         
E         - v5.2
E         + niji 6

tests/integration/test_workflow.py:106: AssertionError
________________________________________________________________________________________________ test_error_workflow _________________________________________________________________________________________________

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
        with pytest.raises(ValueError):
            process_prompt("photo --ar")  # Missing value
    
        # Test invalid style
        with pytest.raises(ValueError):
            process_prompt("photo --style invalid")  # Invalid style value
    
        # Test invalid version
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE <class 'ValueError'>

tests/integration/test_workflow.py:178: Failed
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
        results = process_prompt(prompt)
    
        # 2x2x2 = 8 permutations
        assert len(results) == PERMUTATION_COUNT_2X2X2
    
        # Check common attributes
        for result in results:
            assert len(result.image_prompts) == 2
            assert result.aspect_width == ASPECT_WIDTH
            assert result.aspect_height == ASPECT_HEIGHT
            assert result.stylize == STYLIZE_VALUE
            assert result.chaos == CHAOS_VALUE
>           assert result.version == "v5.2"
E           AssertionError: assert None == 'v5.2'
E            +  where None = MidjourneyPrompt(text='a vintage portrait with warm tones', image_prompts=[ImagePrompt(url='https://example.com/img1.jpg'), ImagePrompt(url='https://example.com/img2.jpg')], stylize=100, chaos=50, weird=None, image_weight=None, seed=None, stop=None, aspect_width=16, aspect_height=9, style='raw', version=None, personalization=None, quality=1.0, character_reference=[], character_weight=100, style_reference=[], style_weight=None, style_version=None, repeat=None, turbo=True, relax=False, tile=False, negative_prompt=None, extra_params={}).version

tests/integration/test_workflow.py:209: AssertionError
================================================================================================== warnings summary ==================================================================================================
tests/engines/test_base.py:14
  /Users/adam/Developer/vcs/github.twardoch/pub/twat-packages/midjargon/tests/engines/test_base.py:14: PytestCollectionWarning: cannot collect test class 'TestPrompt' because it has a __init__ constructor (from: tests/engines/test_base.py)
    class TestPrompt(BaseModel):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================================================================================ slowest 10 durations ================================================================================================
0.17s call     tests/engines/midjourney/test_parser.py::test_extra_parameters
0.06s call     tests/cli/test_main.py::test_image_url_handling
0.06s call     tests/cli/test_main.py::test_basic_prompt
0.06s call     tests/cli/test_main.py::test_complex_prompt
0.05s call     tests/cli/test_main.py::test_no_color_output
0.05s call     tests/cli/test_main.py::test_json_output_formatting
0.05s call     tests/cli/test_main.py::test_raw_output
0.05s call     tests/cli/test_main.py::test_permutations
0.00s call     tests/integration/test_workflow.py::test_complex_workflow
0.00s call     tests/cli/test_main.py::test_invalid_input
============================================================================================== short test summary info ===============================================================================================
FAILED tests/core/test_parameters.py::test_invalid_parameters - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/engines/midjourney/test_parser.py::test_extra_parameters - AssertionError: assert {'flag': None} == {'unknown': 'value', 'flag': None}
  
  Common items:
  {'flag': None}
  Right contains 1 more item:
  {'unknown': 'value'}
  
  Full diff:
    {
        'flag': None,
  -     'unknown': 'value',
    }
FAILED tests/engines/test_base.py::test_engine_with_empty_prompt - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/integration/test_workflow.py::test_parameter_workflow - AssertionError: assert 'niji 6' == 'v5.2'
  
  - v5.2
  + niji 6
FAILED tests/integration/test_workflow.py::test_error_workflow - Failed: DID NOT RAISE <class 'ValueError'>
FAILED tests/integration/test_workflow.py::test_complex_workflow - AssertionError: assert None == 'v5.2'
 +  where None = MidjourneyPrompt(text='a vintage portrait with warm tones', image_prompts=[ImagePrompt(url='https://example.com/img1.jpg'), ImagePrompt(url='https://example.com/img2.jpg')], stylize=100, chaos=50, weird=None, image_weight=None, seed=None, stop=None, aspect_width=16, aspect_height=9, style='raw', version=None, personalization=None, quality=1.0, character_reference=[], character_weight=100, style_reference=[], style_weight=None, style_version=None, repeat=None, turbo=True, relax=False, tile=False, negative_prompt=None, extra_params={}).version
====================================================================================== 6 failed, 60 passed, 1 warning in 1.19s =======================================================================================