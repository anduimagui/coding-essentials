---
name: local-code-review
description: Review local repository changes before commit or handoff, including staged, unstaged, untracked, and recent local commits. Use when asked to check local changes, review work in progress, summarize what changed, split local work into coherent sections, identify risks, or prepare a concise local-change handoff.
---

# Local Code Review

Use this skill to inspect the current worktree and explain the local work clearly before commit, PR, or handoff. Combine a bug-first review with a structured summary of what changed.

## Workflow

1. Identify the repository root and read local instructions before judging the diff.
2. Determine the review scope:
   - Uncommitted work: staged, unstaged, and untracked files.
   - Local commits: commits ahead of the upstream branch when present.
   - Explicit scope from the user: a path, file set, commit range, or supplied diff.
3. Inspect local state with focused commands:

```bash
git status --short
git diff --stat
git diff --cached --stat
git diff --name-status
git diff --cached --name-status
git ls-files --others --exclude-standard
```

4. Read the changed files and nearby code paths needed to understand behavior. For untracked files, inspect the file itself and where it is referenced.
5. Group the work into coherent sections by purpose, not by file order. Examples: API behavior, persistence/schema, UI, tests, docs, tooling, generated assets, cleanup, release config.
6. Review for correctness, regressions, missing tests, risky assumptions, data loss, security issues, broken docs, and accidental scope creep.
7. Run focused verification when practical. If verification is not run, state the gap directly.
8. Do not stage, commit, delete, or rewrite files unless the user explicitly asks.

## Review Checks

- Local state: staged versus unstaged mismatch, untracked files that look intentional, ignored files that should remain local, and generated files that may not belong.
- Behavior: edge cases, error paths, compatibility, public API changes, migrations, time zones, concurrency, ordering, and cleanup.
- Tests: coverage for changed behavior, weak assertions, missing failure cases, stale snapshots, and untested config or script changes.
- Handoff clarity: whether the local work can be explained as a few coherent sections, or whether unrelated work should be split before commit.

## Output

Lead with actionable findings ordered by severity. Each finding should include a tight file/line reference when possible, impact, and fix direction.

Then summarize the local work in sections:

```text
Findings
- [P1] path/to/file.ts:42 - Impact and concrete fix direction.

Local Work Sections
- API behavior: files touched and what changed.
- Tests: coverage added or missing.
- Tooling/docs: scripts, metadata, or documentation changes.

Verification
- Ran: command and result.
- Not run: command or check, with reason.

Residual Risk
- Anything still uncertain or worth checking before commit.
```

If there are no actionable findings, say that directly before the sectioned summary.
