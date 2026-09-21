---
name: pull-request-review
description: Review code changes with a bug-first engineering stance. Use when asked to review a pull request, branch diff, staged changes, patch, or recent commit for regressions, missing tests, risky behavior, incorrect assumptions, or maintainability issues.
---

# Pull Request Review

Use this skill to review changes as if they are about to merge. Prioritize correctness, regressions, security, data loss, compatibility, and missing tests over style preferences.

## Workflow

1. Inspect repository instructions and the target diff before forming conclusions.
2. Determine the intended behavior from the issue, PR description, commit messages, changed files, and nearby code.
3. Review changed code paths and their callers, not only the edited lines.
4. Check tests, docs, migrations, generated files, and release notes when relevant.
5. Run focused verification when practical, or state clearly what was not run.
6. Report only actionable findings. Avoid low-value nits unless they mask a real bug.

## Review Checks

- Correctness: edge cases, null/empty states, concurrency, error handling, time zones, ordering, and resource cleanup.
- Compatibility: public API changes, schema changes, migration safety, CLI flag behavior, config defaults, and persisted data.
- Security: auth, permissions, secrets, injection, unsafe deserialization, logs, and dependency exposure.
- Testing: missing regression tests, weak assertions, untested failure paths, and brittle fixtures.
- Maintainability: misplaced ownership, unclear names, excessive coupling, and comments that no longer match behavior.

## Output

Lead with findings ordered by severity. Each finding should include a tight file/line reference when possible, the impact, and the concrete fix direction.

If there are no findings, say so directly and mention any residual risk or verification gap.
