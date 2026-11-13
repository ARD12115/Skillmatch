# Product Requirements Document (PRD) — SkillMatch

**Event:** CSE-HackSpark-2026, Stage 1 (Class-Level), 13 Nov 2026, 9:30 AM - 4:30 PM
**Theme:** 3 — AI for Everyday Life
**Problem statement:** Basic Resume Screening and Skill Matching System
**Core theme (carried through Stages 2-3):** Student employability and skill development
**Team:** <Team name> · Leader: <name> · Mentor: <faculty guide>

## 1. Overview
Students often don't know why their resumes get rejected or which skills they're missing for a role. SkillMatch reads a resume, compares it to a job description (JD) or a preset role, and returns a match score, matched skills, missing skills and a plain-language explanation.

## 2. Problem
- Students apply to roles without knowing how well their resume fits.
- Keyword-only checks miss synonyms ("ML" vs "machine learning").
- Placement cells screen many resumes by hand, which is slow and inconsistent.
- Existing ATS tools are opaque: a score with no reasons.

## 3. Target users
| User | Need |
|---|---|
| Student (primary) | Check fit for a role, see exactly what to add or learn |
| Placement cell / faculty (secondary) | Quickly shortlist and compare several resumes for one role |

## 4. Goals and non-goals
**Goals**
1. Working prototype in one sitting: upload -> score -> explanation.
2. Explainable output (why this score, which skills matter).
3. Runs locally, offline, with no resume data leaving the machine.
4. Measured accuracy on ~20 test resumes (feeds Stage 2 "test results").

**Non-goals (Stage 1)**
Learning paths, quizzes, LLM chat, user accounts, database, deployment, hiring decisions.

## 5. User stories
- As a student, I upload my resume and paste a JD so I can see my match score.
- As a student, I see which required skills I'm missing so I know what to add.
- As a student, I see the evidence (where in my resume a skill was found) so I trust the result.
- As a placement officer, I upload several resumes for one JD and see them ranked.

## 6. Functional requirements (MoSCoW)
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | Upload resume as PDF (text-based) | Must |
| FR-2 | Extract plain text; show friendly error for scanned/empty PDFs | Must |
| FR-3 | Input JD by paste, or choose a preset role (e.g. Python Developer, Data Analyst, Web Developer) | Must |
| FR-4 | Extract skills from resume and JD using a curated taxonomy with aliases | Must |
| FR-5 | Compute match score 0-100 with documented formula | Must |
| FR-6 | Show matched skills, missing skills, extra skills | Must |
| FR-7 | Explanation panel: score breakdown and evidence snippets | Must |
| FR-8 | Semantic matching (embeddings) with TF-IDF fallback | Should |
| FR-9 | DOCX upload | Should |
| FR-10 | Batch mode: rank multiple resumes for one JD, CSV export | Should |
| FR-11 | Suggestions: "add these N skills to raise your score" | Could |
| FR-12 | Download report (CSV/Markdown) | Could |

## 7. Non-functional requirements
- Score + results in under 5 seconds for a typical 2-page resume (after model load).
- Works with Wi-Fi off after setup.
- No persistence of resume text by default.
- Clear error messages; the app never shows a stack trace to the user.
- Responsible use: framed as decision support, not an automated hiring decision (see security.md).

## 8. Success metrics
| Metric | Target |
|---|---|
| Skill extraction recall on test resumes | >= 80% |
| Skill extraction precision | >= 85% |
| Rank agreement with manual judgement (resumes vs one JD) | Top-3 overlap >= 2/3 |
| Demo runs end-to-end without error | 100% on rehearsal |

## 9. Evaluation rubric mapping (100 marks)
| Criterion | Marks | How we earn it |
|---|---|---|
| Problem Identification and Relevance | 15 | Student employability story, Rule 7 definition (problem-definition.md) |
| Innovation and Originality | 20 | Semantic matching, explainable scores, evidence snippets (not plain CRUD) |
| Technical Implementation | 25 | Layered pipeline, embeddings + fallback, tested modules |
| Working Prototype and Demonstration | 20 | Live demo with real sample resumes |
| Practical Feasibility and Impact | 10 | Offline, free tools, measured accuracy |
| Teamwork and Presentation | 10 | Clear roles, rehearsed 5-minute demo |

## 10. Deliverables (Stage 1)
Basic working prototype · source code · problem description · 5-minute demonstration.

## 11. Risks
| Risk | Mitigation |
|---|---|
| Resume PDFs with messy layouts (two columns) | Test several formats early; use pdfplumber with a PyMuPDF fallback if needed |
| Scanned PDFs have no text | Detect and show "text-based PDFs only" message; OCR is a Stage 2 idea |
| Judges say "just keyword matching" | Demonstrate taxonomy alias recognition ("ML" -> "Machine Learning") and explain the separate skill-similarity component |
| Embedding model not cached at venue | Pre-download in setup.sh; TF-IDF fallback |
| Resume screening is a popular pick | Differentiate via skill-gap framing and explainability |

## 12. Stage roadmap (summary; details in roadmap.md)
Stage 1 skill gap -> Stage 2 personalized learning path + assessments -> Stage 3 career guidance and skill-gap prediction.
