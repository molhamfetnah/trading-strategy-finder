Spec: Interview Preparation & Deep Documentation
Date: 2026-05-16
Author: Assistant (with user approval)

Goal

Prepare the user (candidate, Data Scientist) to present the Ultimate Dashboard project in a final interview. Deliver a comprehensive interview playbook plus deep, per-file documentation for core project components so the candidate can explain implementation details, design choices, trading concepts, and reproduce demos.

Scope

- Core files only (as approved):
  - ultimate_dashboard.py
  - src/backtest/engine.py
  - src/signals/ml_filter.py
  - src/indicators/scalping.py
  - src/data/loader.py
  - main.py
  - tests/test_ultimate_dashboard.py
  - README and docs/dashboard_data.json + dashboard HTML (overview)

- Deliverables (stage A -> stage B):
  1. Interview_Playbook.md: talking points, demo script, slide outline, key metrics, and Q&A
  2. Per-file deep docs (expanded Project_Documentation/*.doc.md) with:
     - high-level summary, purpose, inputs/outputs
     - section-by-section explanation
     - line-by-line commentary for complex blocks
     - academic appendix (indicator math, ML rationale, backtest economics)
     - cross-references to tests and related modules
  3. Practice kit: common/interview-specific questions + model answers, flashcards, timed mock sessions
  4. Demo artifacts checklist: commands to reproduce dashboard, smoke-test steps, and troubleshooting notes

Approach / Methodology

1. Expand per-file docs: take existing skeletons in Project_Documentation and replace TODOs with deep content. For complex functions, include small code excerpts with explanation and expected values.
2. Create Interview_Playbook.md that maps to per-file docs and provides a concise narrative the candidate can memorize: problem statement, approach, experiments, results, limitations, next steps.
3. Produce a 10–12 slide outline for a 7–10 minute walkthrough: slide bullets for each.
4. Prepare practice questions grouped by difficulty and area (data, indicators, ML, backtest, productionization). Provide succinct model answers and 90s/3min responses.
5. Commit and surface files under docs/interview_preparation/ for easy review.

Per-file doc template (applied to each core file)
- File name & path
- One-line purpose
- Summary (3–5 bullet points)
- API (functions/classes, args, returns)
- Section-by-section explanation (with line ranges)
- Key variables and invariants
- Example inputs/outputs (small DataFrame samples or dicts)
- Tests that validate behavior
- Academic appendix: formulas, citations, intuitive explanation
- Talking points: 3–6 bullets for interview
- Crossrefs: other files/tests to read next

Acceptance criteria
- Interview_Playbook.md present at docs/interview_preparation/Interview_Playbook.md
- All listed core file doc files updated with substantial content (no TODO placeholders)
- A short mock Q&A script and 10 slide outline present
- All changes committed and pushed

Timeline & checkpoints
- Phase 1 (this session): create design spec (this file) and commit. -- DONE
- Phase 2 (next): expand ultimate_dashboard.py doc and Interview_Playbook draft. Ask user to review.
- Phase 3: expand remaining core files and prepare practice kit.
- Phase 4: run mock Q&A and iterate on edits.

Review & iteration
- After drafting each artifact, the assistant will prompt the user to review that artifact (one at a time).
- Changes requested will be applied and re-committed.

Reversal plan
- All docs are additive; revert using git revert <commit> or restore individual files from docs/legacy if needed (standard git commands listed in ARCHIVE_ACTIONS.md).

Next action
- Expand the ultimate_dashboard.py doc and draft Interview_Playbook.md, then commit and ask for your review.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
