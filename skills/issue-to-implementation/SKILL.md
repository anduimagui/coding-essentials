---
name: issue-to-implementation
description: Turn a remote GitHub or GitLab issue filed by someone else into a focused implementation with tests, docs, and verification. Use when asked to implement an issue, bug report, feature request, or ticket from a remote repository that the user did not author. Trigger on phrases like "implement this issue", "address this ticket", "fix this bug report", "work on this feature request", or when the user provides a GitHub/GitLab issue URL or number belonging to another person's issue. Do not trigger for the user's own local tasks, notes, or self-authored requirements.
---

# Issue to Implementation

Use this skill to turn a remote issue (GitHub, GitLab, or other public tracker) filed by someone else into a verified code change. The issue author is not the user — read the full remote context before touching code so the implementation matches what the reporter and maintainers actually asked for.

## Workflow

1. Fetch the full issue from the remote tracker. Use `gh issue view <number>` for GitHub issues. Read the body, comments, linked PRs, labels, milestone, assignees, and any closing references. Capture acceptance criteria, reproduction steps, screenshots, logs, and environment details from the issue thread.

2. Inspect the local repo instructions and current worktree state. Check `AGENTS.md`, `README*`, `CONTRIBUTING*`, and recent commit style.

3. Trace the relevant implementation path with `rg`, tests, callers, routes, commands, or public exports. Map the issue's requirements to the codebase.

4. Identify the minimal behavior change and the files that own it. Scope the change to what the issue asks for — do not add unrelated improvements or refactors.

5. Implement using existing patterns and local abstractions. Match the code style of the surrounding files.

6. Add or update focused tests that cover the issue's acceptance criteria. Update docs or generated files only when the user-facing behavior changes or repo convention requires it.

7. Run targeted verification first (the affected module's tests), then broader checks when the blast radius warrants it.

## Scope Control

- Do not mix unrelated refactors into feature work.
- Preserve unrelated local changes in the worktree.
- If the issue has conflicting requirements, missing reproduction steps, or unclear intent, ask the user for clarification before implementing.
- Prefer small commits and explicit verification notes for reviewability.

## Output

Summarize the issue number, what was implemented, files changed, tests added/modified, and any follow-up work that remains outside the requested scope.
