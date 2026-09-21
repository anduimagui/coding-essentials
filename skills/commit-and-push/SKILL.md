---
name: commit-and-push
description: Commit and push only the changes made in the current work session while preserving unrelated worktree changes, including files that may be changing concurrently outside this context. Use when asked to commit, push, publish, save work in git, or prepare a clean commit without agent self-credit in the branch name, committer identity, or commit message.
---

# Commit and Push

Use this skill to publish only the work from the current work session. Do not add agent branding, self-credit, or similar attribution to the commit message or committer identity.

## Required Preflight

Before any command that changes history, reads/writes remotes, or depends on a hosting account:

1. Identify the active repository root with `git rev-parse --show-toplevel`.
2. Verify identity before acting:
   - `git config user.name`
   - `git config user.email`
   - `git remote -v`
   - `gh auth status` or the relevant hosting CLI account
3. Continue only when the active identity and remote match the intended repository account.

Never print secrets, tokens, private keys, or credential-helper output.

## Commit Workflow

The folder may be actively changing during the session: another agent, terminal, IDE, or background process could be editing files outside this current context. Treat the worktree as possibly concurrent, identify this session's files precisely, and re-verify state before each staging decision. Never assume the worktree is frozen.

### Recognizing concurrent work

A `git status` or `git diff` read is a snapshot, not a guarantee. If two successive reads disagree — a file flipped from modified to deleted, a new file appeared, a name changed, or the index now holds a rename you never staged — that is external concurrent activity. Do not treat it as a mystery to explain.

When state changes under you:

- Do not re-derive "what happened" from history. Asking `did the merge delete this?` or reading `git log` to attribute a change is wasted effort; another process changed it, and the response is the same regardless of its identity.
- Re-snapshot with `git status --short` and act only on the latest read.
- Scope to the files you actually edited in this session. Anything you did not touch in-context — modified, deleted, renamed, or newly staged — is someone else's work. Leave it out even when you cannot explain where it came from.
- Treat the index as shared. `git diff --cached --name-status` may show a rename, add, or delete that was staged by another process, not by you. Do not commit it unless it is clearly part of your session's scope.
- Define "this session's files" when you stage, not from a remembered earlier snapshot. The safe scope is the list of paths you changed in this conversation.

1. Inspect the worktree and recent style:

```bash
git status --short
git diff
git log -5 --oneline
```

2. Check the remote mainline before staging or committing anything:

```bash
git fetch --prune
git branch --show-current
git symbolic-ref refs/remotes/origin/HEAD
git log --oneline HEAD..origin/main
git merge-base --is-ancestor origin/main HEAD
```

Use the repository's default branch instead of `origin/main` when it differs. If remote mainline has new commits that are not in the current branch, run a merge-readiness check from the current branch before committing. Prefer a non-destructive check such as `git merge-tree` when possible, or a temporary worktree if a full merge check is needed.

- If the merge-readiness check finds conflicts, test failures, dependency updates, schema changes, generated-file changes, lockfile changes, API changes, or other likely breaking changes from remote mainline, stop before staging or committing. Warn the user with the exact files and commands that showed the risk, then wait for direction.
- If remote mainline is already contained in the current branch, or the merge-readiness check is clean and does not show likely breaking changes, continue.

3. Identify the exact files changed by the current work session. Exclude unrelated modified or untracked files from other sessions or user work.
4. Check whether repository conventions require official follow-up files in the same commit, such as changelogs, release notes, version fields, generated docs, lockfiles, or package metadata. Include them only when the repository clearly expects them for this change.
5. Stage explicitly:

```bash
git add -- path/to/file another/path
```

Do not use `git add .` or `git commit -a`.

6. Re-check the worktree and index immediately before committing. Files outside this session may have changed since the initial inspection, and the index may contain entries staged by another process:

```bash
git status --short
git diff --cached --stat
```

If anything new, unrelated, or unexpected has appeared — including a rename, add, or delete that you did not stage — unstage it (`git restore --staged -- <file>`) and stage or unstage accordingly before proceeding.

7. Commit with a clean, descriptive message that reads naturally and contains no agent self-credit.
8. Re-check remote mainline before push, then integrate and push only if the check still passes:

```bash
git pull --rebase --autostash
git push
git status --short --branch
```

9. Leave unrelated local changes — including any concurrent work that appeared during the session — untouched.

## Reporting

In the final response, provide:

- A simple title for the work.
- One short sentence explaining what was done.
- How the commit was isolated to the current work session's files.
- Whether any official repo-wide follow-up files were included.
- Any concurrent work that appeared during the session and was left untouched.
- Any push or identity blocker, with the verification command that failed.
