# Test Plan — SkillMatch

## 1. Unit tests (pytest)
| Module | Cases |
|---|---|
| validators | wrong extension, wrong magic bytes, oversize, empty file, valid PDF |
| pdf_parser | normal PDF, two-column PDF, image-only PDF (expects `EmptyDocumentError`) |
| extractor | canonical name, alias ("ML"), case, `C++`/`C#`/`Node.js`, typo, duplicates, no skills |
| jd_parser | required vs preferred sections, JD with no sections |
| scorer | all matched = ~100, none matched = low, ordering (closer resume scores higher), no-preferred redistribution |
| similarity | identical text ~1.0, unrelated text low, fallback path works when embeddings are off |

## 2. Evaluation set (for "test results")
1. Collect separate **synthetic or consented** tuning and evaluation resume sets, with no overlap. Use the tuning set to develop aliases and adjust `WEIGHTS`.
2. Before evaluating, freeze the taxonomy, aliases, and weights. Reserve an unseen set of ~20 resumes (mix of CSE branches, strong/average/weak) for evaluation only.
3. Pick 2-3 JDs (e.g. Python Developer, Web Developer, Data Analyst); for each evaluation resume, have a team member list true skills by hand as ground truth.
4. Run extraction on the unseen evaluation set and compute precision and recall per resume and on average. Do not use these evaluation results to retune the same run.
5. Manually rank 5 evaluation resumes per JD; compare with the system's ranking (top-3 overlap).
6. Report only metrics from the unseen evaluation set in the presentation. Any changes informed by those results require a new unseen evaluation set.

| Resume | True skills | Found | Precision | Recall |
|---|---|---|---|---|
| R01 | | | | |

## 3. Manual / demo tests
- Wi-Fi off run-through.
- Two-column and one-column resume.
- Scanned PDF (graceful error).
- 6 MB file (rejected cleanly).

## 4. Definition of done
All Must requirements pass, `pytest -q` is green, the demo has been rehearsed twice end to end.
