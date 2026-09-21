---
name: git-conflict-resolution
description: Resolve git merge and rebase conflicts against the branch the current work is actually intended to merge into. Use when asked to fix merge conflicts, rebase conflicts, PR branch conflicts, sync a branch with its PR base, merge upstream into a feature branch, or explain and resolve conflicted files without assuming the target branch is main.
---

# Git Conflict Resolution

Use this skill to resolve merge or rebase conflicts in a repository while preserving the branch's intended feature work and the target branch's upstream changes.

## Required Preflight

Before any command that changes history, reads or writes remotes, or depends on a hosting account:

1. Identify the active repository root with `git rev-parse --show-toplevel`.
2. Read repository instructions such as `AGENTS.md`, `CLAUDE.md`, or equivalent local guidance.
3. Check for an applicable `.envrc` in the repository root or parent path.
4. If `.envrc` exists and `direnv` is available, load it in the active shell, for example `eval "$(direnv export zsh)"` or `eval "$(direnv export bash)"`.
5. If direnv reports blocked, stale, or not allowed, stop and ask before running `direnv allow`.
6. Verify identity before remote or history actions:
   - `git config user.name`
   - `git config user.email`
   - `git remote -v`
   - `gh auth status` or the relevant hosting CLI account
7. Continue only when the active identity and remote match the intended repository account.

Do not print secrets, tokens, private keys, or credential-helper output.

## Determine the Target Branch

Determine the branch to merge or rebase against in this order:

1. Use a branch explicitly named by the user.
2. If a GitHub PR URL or number is provided, query the PR with `gh` and use the PR base branch.
3. If the current branch has an open PR, use the PR base branch.
4. Use the current branch's configured merge or tracking target only when it is the intended integration branch, not merely the branch's own remote copy.
5. Use the remote default branch only as a fallback when no better merge target is available.

Never assume the target branch is `main`, `master`, or the remote default branch when the PR base or another integration branch is available.

## Sync the Local Branch First

1. Inspect branch and remote state:

```bash
git status --short --branch
git branch --show-current
git branch -vv
git remote -v
```

2. If a PR URL or number is provided, query it and verify the head/base mapping:

```bash
gh pr view <pr> --json headRefName,baseRefName,headRepositoryOwner,headRepository,number,url
```

3. Confirm the current branch matches the PR head branch. If not, check out the correct PR branch before resolving conflicts.
4. If the current branch tracks its own remote branch and is behind, pull that branch locally before merging or rebasing the target branch.
5. Fetch the real target branch after identity and direnv preflight succeeds.

## Expose Real Conflicts

Start the merge or rebase in a way that shows conflicts without prematurely committing. For merges, prefer avoiding an automatic commit:

```bash
git merge --no-commit --no-ff <remote>/<target-branch>
```

For rebases, use the repository's normal branch workflow and stop at conflicts naturally:

```bash
git rebase <remote>/<target-branch>
```

After the operation stops, identify true conflicted files:

```bash
git diff --name-only --diff-filter=U
git status --short
```

Distinguish unresolved conflict files from the large normal change set introduced by the merge or rebase.

## Explain Each Conflict

For each conflicted file:

1. Inspect both sides and the base when available:

```bash
git show :1:<file>
git show :2:<file>
git show :3:<file>
```

Stage `:1:` is the merge base, `:2:` is ours, and `:3:` is theirs. Use temporary copies, `git diff`, or index stages to inspect without destroying work. Do not run checkout commands that overwrite a file unless you intend that resolution.

2. Explain:
   - what the current branch changed
   - what the target branch changed
   - why the changes conflict
   - whether the likely resolution is local, upstream, combined, or custom

## Resolve Conflicts

Resolve each file directly and preserve the intent of both sides where appropriate:

- Keep local changes when the current feature work should win.
- Take upstream changes when the target branch's refactor, fix, or deletion supersedes local work.
- Combine both when the feature still matters and upstream changed the surrounding structure.
- Write a custom resolution when neither side is correct as-is.

Prefer keeping upstream refactors, dependency updates, generated structure, or shared APIs intact while reapplying the local branch's intended behavior on top.

## Verify the Final State

Before declaring the conflict resolved:

1. Confirm conflict markers are gone:

```bash
rg '^(<<<<<<<|=======|>>>>>>>)'
```

2. Confirm no unresolved files remain:

```bash
git diff --name-only --diff-filter=U
git status --short
```

3. Review edited files with merge-safety checks:

```bash
git diff --check
git diff -- <resolved-files>
```

4. Run relevant tests, typechecks, builds, or linters from the correct package directories. Do not assume commands run from the repository root.
5. If dependency or lockfile changes were merged, refresh/install dependencies before running verification.

## Complete the Merge or Rebase Only When Asked

If the user asks to commit, complete the merge or rebase using the repository's existing commit style. If the user asks to push, push the branch normally without bypassing hooks.

If push fails because hooks, typechecks, or tests fail after the merge, fix the environment first when appropriate, rerun checks, then push again.

## Conflict Prevention Suggestions

When conflicts occur in large or frequently edited files, suggest refactors only when they are within the scope or purpose of the current branch or pull request.

Do not recommend unrelated cleanup outside the changed files or the PR context.

Prefer suggestions that materially reduce future conflict risk, such as extracting:

- isolated command groups
- config maps
- helpers
- docs metadata
- feature-specific logic
- shared sources of truth used by both code and docs

For each worthwhile suggestion, explain:

- which file is conflict-prone
- what should move out
- where it should move
- why that would reduce future conflicts against the target integration branch

Avoid churn for trivial files.

## Final Response

Summarize:

- target branch used and how it was determined
- conflicted files resolved
- chosen resolution strategy per file
- verification commands and results
- any remaining blocker
- focused conflict-prevention suggestions, if worthwhile

If the merge or rebase is not fully completed, remind the user to run the relevant remaining steps: `git add <files>`, `git commit` or `git rebase --continue`, tests/typechecks, and `git push` when needed.
