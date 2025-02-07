Fix the issues in this order. After each fix, run the tests to ensure that the issue is fixed. Then remove that task from the text in @TODO.md 


# TASK 3

> 2. Robust Parameter Validation (Midjourney level only): • For parameters like the conflicting flags "--v 5.2" vs "--niji 6", the test requires that the first one wins. Our parser is mistakenly allowing the second flag ("--niji") to override the version. We need to update the parameter parsing logic in the midjourney parser so that once version is set (by "--v"), subsequent "--niji" parameters do not overwrite it.

YES! Change it

# TASK 4

> 3. Engine Behavior for Empty Prompts: • The test for an empty prompt (in test_engine_with_empty_prompt) expects a ValueError. According to your instructions, an empty prompt must raise a ValueError, so we should adjust the engine's behavior if it isn't already raising an error.

YES! Fix it

# TASK 5

> • Also, some tests for parameter validation (e.g. invalid parameters) indicate that malformed inputs should trigger a ValueError. We have to ensure that our midjourney-level validation is enforcing these rules, even if our core parser itself is more relaxed.

YES! 



