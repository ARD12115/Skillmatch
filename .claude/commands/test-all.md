---
description: Run lint and the full test suite, then summarize failures
---
Run `ruff check .` and `pytest -q`. If anything fails, explain the root cause in one or two lines per failure and propose the smallest fix. Do not change tests just to make them pass.
