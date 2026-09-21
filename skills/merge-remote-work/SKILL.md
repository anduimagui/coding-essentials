---
name: merge-remote-work
description: Merge remote work from the current branch's configured upstream before making changes. Use when the current branch is the branch to preserve and work should start from the latest remote state without switching branches.
---

# Merge Remote Work

Use this skill when the user wants the current branch treated as the core branch for the task. The first Git action is to merge remote work from its upstream into that branch, then make the requested change on top of that state.

Do not switch branches unless the user asks for that explicitly.

## Required Preflight

Before changing files, history, or remote state:

1. Identify the repository root with `git rev-parse --show-toplevel`.
2. Read repository instructions, especially `AGENTS.md` guidance for direnv, generated files, staging, validation, and remote identity.
3. Check the current branch:

   ```bash
   git branch --show-current
   git status --short --branch
   ```

4. Verify that the current branch has a configured upstream:

   ```bash
   git rev-parse --abbrev-ref --symbolic-full-name @{u}
   ```

5. Verify identity before remote or history-changing actions:

   ```bash
   git config user.name
   git config user.email
   git remote -v
   gh auth status
   ```

   Use the relevant hosting CLI instead of `gh` for non-GitHub repositories.

Never print secrets, tokens, private keys, or credential-helper output.

## Merge Remote Work First

Fetch and merge the current branch's upstream into it before doing the requested work:

```bash
git fetch --prune
git pull --rebase --autostash
git status --short --branch
```

If the branch has no upstream, stop before making changes and ask the user which remote branch should be used. Do not invent an upstream or switch branches.

If the pull reports conflicts, stop and resolve them only when that is within the user's requested task. Otherwise report the conflict files and ask how to proceed.

If local unrelated changes are present, preserve them. Prefer `git pull --rebase --autostash`; if autostash cannot protect the worktree cleanly, stop before overwriting or resetting anything.

## Work On The Current Branch

After remote work is merged:

1. Make only the requested changes on the current branch.
2. Run the repository's required validation or the smallest meaningful validation for the change.
3. Inspect the diff and keep unrelated user work out of the result.
4. Stage explicit paths only; do not use `git add .` or `git commit -a`.
5. If asked to commit or push, re-run `git status --short --branch`, then use the current branch and its upstream for pull and push.

## Reporting

In the final response, include:

- The current branch name and the remote branch merged into it.
- The merge command that succeeded, or the blocker that stopped work.
- The files changed for the requested task.
- The validation command that passed, or the reason validation was not run.
