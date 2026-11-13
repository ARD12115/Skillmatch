# Problem Definition (Rule 7) — SkillMatch

**Statement:** Basic Resume Screening and Skill Matching System (Theme 3: AI for Everyday Life)
**Core theme for all stages:** Student employability and skill development

## Target users
1. Engineering students preparing for internships and placements (primary).
2. Placement cell coordinators and faculty who shortlist resumes (secondary).

## Existing challenges
- Students don't know which skills a job needs or which ones their resume lacks.
- Plain keyword filters miss equivalent terms ("ML" vs "machine learning") and give no reasons.
- Commercial ATS tools are paid, opaque, and send personal data to third-party servers.
- Manual shortlisting by placement staff is slow and inconsistent across reviewers.

## Proposed solution
A local web app where a user uploads a resume and provides a job description or picks a preset role. The system extracts skills using a curated taxonomy, scores the match with a transparent formula (required skills, preferred skills, semantic similarity), and shows matched, missing and extra skills with evidence and a plain-language explanation. Batch mode ranks several resumes against one role.

## Expected outcomes
- A student sees within seconds how well they fit a role and exactly which skills to add.
- Placement staff shortlist faster with consistent, explainable scores.
- No personal data leaves the user's machine.
- Measurable quality: >= 80% recall and >= 85% precision on skill extraction over ~20 test resumes.

## How it grows
Stage 1: find the gap. Stage 2: close the gap (learning paths + assessments). Stage 3: plan the career (role guidance + skill-gap prediction). See roadmap.md.
