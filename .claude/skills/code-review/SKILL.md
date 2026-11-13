---
name: code-review
description: Reviews Python changes in SkillMatch for correctness, layering, type safety, and test coverage. Use when asked to review code or a diff.
---
# Code review checklist
1. Layering: UI has no business logic; matching does not import UI.
2. Public functions have type hints and docstrings.
3. Edge cases handled: empty text, scanned/image-only PDF, very long resume, non-English text.
4. No PII in logs or exceptions.
5. Tests exist for new behaviour and cover at least one failure case.
Output: Must fix / Should fix / Nice to have.
