PROBLEM: 

I did

`python -m midjargon fal "hello" -j`

I got

```
{
  "images": [],
  "prompt": "hello"
}ERROR: Could not consume arg: fal
Usage: __main__.py

For detailed information on this command, run:
  __main__.py --help
```

The correct output is the initial JSON, so it kind of works but then produces this `ERROR: Could not consume arg: fal
Usage: __main__.py

For detailed information on this command, run:
  __main__.py --help` which wasn't there earlier today. 

TASK: Fix the PROBLEM.

