# Archive actions: moved legacy/unreferenced files to docs/legacy/

Date: 2026-05-16T17:36:09+03:00

Summary:
- A set of files that were not referenced anywhere in the codebase (heuristic grep scan) were moved into docs/legacy/ to keep the repository tidy while preserving history.

Files moved (before -> after):

- .github/copilot-instructions.md -> docs/legacy/copilot-instructions.md
- AGENTS.md -> docs/legacy/AGENTS.md
- CHANGELOG.md -> docs/legacy/CHANGELOG.md
- docs/COMPREHENSIVE_BUG_REPORT.md -> docs/legacy/COMPREHENSIVE_BUG_REPORT.md
- docs/COUNCIL_REPORT-round3-FINAL.md -> docs/legacy/COUNCIL_REPORT-round3-FINAL.md
- docs/COUNCIL_REPORT-round3.md -> docs/legacy/COUNCIL_REPORT-round3.md
- docs/COUNCIL_REVIEW_v1.1-round2_EXPORTED.md -> docs/legacy/COUNCIL_REVIEW_v1.1-round2_EXPORTED.md
- docs/COUNCIL_REVIEW_v1.1.md -> docs/legacy/COUNCIL_REVIEW_v1.1.md
- docs/COUNCIL_REVIEW_v1.1_EXPORTED.md -> docs/legacy/COUNCIL_REVIEW_v1.1_EXPORTED.md
- docs/COUNCIL_REVIEW_v1.1_UPDATED.md -> docs/legacy/COUNCIL_REVIEW_v1.1_UPDATED.md
- docs/CRITICAL_TIMESTAMP_BUG.md -> docs/legacy/CRITICAL_TIMESTAMP_BUG.md
- docs/index.html -> docs/legacy/index.html
- docs/report-revision4.md -> docs/legacy/report-revision4.md
- docs/report-revision5.md -> docs/legacy/report-revision5.md
- docs/ultimate_trading_dashboard_analysis.md -> docs/legacy/ultimate_trading_dashboard_analysis.md
- docs/ultimate_trading_dashboard_final_review.md -> docs/legacy/ultimate_trading_dashboard_final_review.md
- docs/ultimate_trading_dashboard_re_review.md -> docs/legacy/ultimate_trading_dashboard_re_review.md
- parameter_optimizer.py -> docs/legacy/parameter_optimizer.py
- task.md -> docs/legacy/task.md
- docs/superpowers/ -> docs/legacy/superpowers/

Rationale and decision method:
- Method: ran a repository-wide basename grep to find files whose filenames are not referenced elsewhere in the repo. This is a heuristic intended to identify documentation and scripts that appear unused by the code paths.
- Files identified are generally documentation, exported review artifacts, or older scripts. Some false positives are possible (standalone docs, changelogs, or external references).
- Action choice: archive (move) into docs/legacy/ to preserve their history while removing noise from top-level and primary docs directories.

Before/After (how repo structure changed):
- Before: files lived at their original paths (listed above).
- After: files are located under docs/legacy/ (flattened by basename for root/docs files; directory preserved for docs/superpowers/).

How to reverse this action:

1) If you want to restore a single file to its original location:

   git mv docs/legacy/<basename> <original/path/filename>
   git commit -m "revert(docs): restore <basename> from docs/legacy"
   git push origin HEAD:master

   Example:
   git mv docs/legacy/COUNCIL_REPORT-round3.md docs/COUNCIL_REPORT-round3.md

2) To restore the entire archive (undo commit):

   # Find the commit that performed the archive (shown in commit history). Then:
   git revert <commit-sha>
   git push origin HEAD:master

   Or, if you prefer to move files back manually, use git mv for each file as above.

Notes and recommendations:
- This archive preserves file history (git mv retains history) — no content was deleted.
- Review the docs/legacy/ files to confirm none are still referenced by external systems or automation (CI, website publishing). If a file must remain at its previous path for tooling, restore it.
- Next steps: manually enrich Project_Documentation and, after review, consider deleting docs/legacy or moving selected files into a long-term archived branch.

