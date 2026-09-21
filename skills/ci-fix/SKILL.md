---
name: ci-fix
description: Diagnose and repair failing CI checks with the smallest safe change. Use when asked to fix GitHub Actions, GitLab CI, local test failures, lint failures, typecheck failures, build failures, or release pipeline errors.
---

# CI Fix

Use this skill to turn a failing check into a reproduced diagnosis and a minimal fix. Prefer the exact failing command and logs over guessing.

## Workflow

1. Identify the failing check, command, job, branch, and commit.
2. Collect logs from the local terminal, CI output, or hosting CLI when available.
3. Reproduce locally with the closest focused command before changing code when practical.
4. Classify the failure: code regression, test expectation, environment drift, dependency issue, flaky timing, missing generated file, or configuration problem.
5. Implement the smallest fix that addresses the root cause.
6. Re-run the failing command and one adjacent safety check when practical.
7. Avoid hiding failures by weakening tests or disabling checks unless that is the intended fix and the reason is documented.

## Common Commands

```bash
git status --short --branch
gh run list --limit 10
gh run view --log
npm test
npm run lint
pytest
go test ./...
cargo test
```

Use the commands that match the repo; do not assume a package manager without checking.

## Output

Summarize:

- Failing check and root cause.
- Files changed.
- Verification commands and results.
- Any remaining CI-only risk that could not be reproduced locally.
