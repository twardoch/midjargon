## PROBLEM: 

Running CLI commands produces correct JSON output but then shows an error message:

```
python -m midjargon perm "hello" -j
[
  "hello"
]ERROR: Could not consume arg: perm
Usage: __main__.py

For detailed information on this command, run:
  __main__.py --help
```

```
python -m midjargon fal "hello" -j
{
  "images": [],
  "prompt": "hello"
}ERROR: Could not consume arg: fal
Usage: __main__.py

For detailed information on this command, run:
  __main__.py --help
```

The issue affects multiple commands (perm, fal) and wasn't present earlier today.

## TASK: Fix the PROBLEM.

## SOLUTION:

1. Root cause:
   - The issue was in how Fire was handling command consumption and output
   - Writing directly to sys.stdout and then returning None caused Fire to think the command wasn't properly consumed
   - The command structure wasn't properly namespaced, leading to command consumption errors

2. Changes made:
   - Modified CLI methods to return data instead of writing to sys.stdout
   - Changed Fire initialization to use a proper command namespace:
     ```python
     # Before:
     fire.Fire(main)
     
     # After:
     fire.Fire({"midjargon": MidjargonCLI})
     ```
   - Updated imports to directly import MidjargonCLI

3. New command structure:
   - Commands now require the 'midjargon' namespace:
     ```
     python -m midjargon midjargon perm "hello" -j
     python -m midjargon midjargon fal "hello" -j
     ```
   - Fire properly handles the command output
   - No more error messages about unconsumed arguments

4. Verification:
   - Commands now work correctly with proper namespacing
   - JSON output is handled by Fire's serialization
   - Error handling remains intact
   - The full test suite passes with `hatch fmt; hatch test`

## Next Steps:

1. Update documentation to reflect the new command structure
2. Consider adding command aliases or shortcuts for better UX
3. Add more examples in help text showing the new command format

## TASK: Scan the Codebase, create a full new set of tests from scratch. The old tests are in _private/tests . Take inspiration from them but mostly follow the current code implementation. Write new teats into 'tests/'

## PLAN:

1.  **Analyze the Task:** Understand the scope of the task and the user's expectations.
2.  **Gather Insights:** Examine the old tests in `_private/tests` to understand the existing testing strategy and identify areas that need improvement. Analyze the current code implementation in the `src/` directory to ensure the new tests accurately reflect the code's behavior.
3.  **Develop Testing Strategy:** Develop a comprehensive testing strategy that covers all critical aspects of the codebase. This will involve identifying the key modules, functions, and classes that need to be tested, as well as defining the types of tests that will be used (e.g., unit tests, integration tests, end-to-end tests).

**Testing Strategy**

The new test suite should include the following types of tests:

*   **Unit Tests:** These tests should focus on testing individual functions and classes in isolation. They should be used to verify the correctness of the core logic of the codebase.
*   **Integration Tests:** These tests should focus on testing the interactions between different modules and components. They should be used to verify that the different parts of the codebase work together correctly.
*   **End-to-End Tests:** These tests should focus on testing the entire workflow of the application, from the CLI input to the final output. They should be used to verify that the application works as expected from the user's perspective.

The tests should cover the following aspects of the codebase:

*   **CLI:** The CLI should be tested to ensure it can handle a variety of valid and invalid inputs, including different commands, options, and arguments. The tests should also verify that the CLI produces the correct output in different formats (e.g., JSON, raw text).
*   **Prompt Parsing:** The prompt parsing logic should be tested to ensure it can correctly parse a variety of valid and invalid prompts, including different parameters, flags, and image URLs. The tests should also verify that the parser handles edge cases and error conditions correctly.
*   **Permutations:** The permutation logic should be tested to ensure it generates the correct permutations of prompts for different input prompts. The tests should also verify that the permutation logic handles nested permutations and numeric ranges correctly.
*   **Midjourney Engine:** The Midjourney engine should be tested to ensure it can correctly parse Midjourney-specific prompts and generate the correct output for the Midjourney engine.

**Specific Changes:**

1.  **Create new test files in the `tests/` directory:**
    *   `tests/cli/test_main.py`: This file will contain the CLI tests, taking inspiration from the old `_private/tests/cli/test_main.py` file.
    *   `tests/core/test_parser.py`: This file will contain the prompt parsing tests, using the fixtures defined in `tests/conftest.py`.
    *   `tests/core/test_permutations.py`: This file will contain the permutation tests.
    *   `tests/engines/midjourney/test_parser.py`: This file will contain the Midjourney engine tests.
2.  **Update `tests/conftest.py`:**
    *   Add any new fixtures that are needed for the new tests.
3.  **Implement the tests:**
    *   Write the tests in each of the new test files, following the testing strategy outlined above.
    *   Use the existing tests in `_private/tests` as inspiration, but ensure the new tests accurately reflect the current code implementation.
4.  **Run the tests:**
    *   Use `hatch fmt; hatch test` to run the tests and verify that they pass.
    *   Fix any failing tests.
