---
name: test-writer
description: Writes pytest unit tests for SkillMatch modules, including edge cases. Use when adding or changing parsing, extraction or matching code.
---
# Test writing rules
- One test file per module, named `tests/test_<module>.py`.
- Cover: happy path, empty input, aliases ("ML" vs "machine learning"), duplicate skills, unknown skills.
- Use small synthetic resume strings, not real resumes.
- Scoring tests assert ranges and ordering (a closer resume scores higher), not magic numbers.
