---
name: back-to-main
description: Return to main with local work preserved and remote main incorporated, including work already committed or pushed from another checkout. Also use when already on main but behind origin/main. Do not create new branch commits or push.
---

# Back to Main

Finish on local `main` with the latest fetched `origin/main` incorporated and all unpublished local work preserved. Being on `main` is not enough: a change pushed from another branch or worktree must also reach this checkout.

## Guardrails

- Create no new branch commits (including merge commits), push nothing, and rewrite no existing history. A temporary stash is allowed for preservation.
- Preserve staged, unstaged, and untracked work, including unrelated edits. Keep recovery artifacts until restoration is verified.
- Remote-ahead commits are work to incorporate, not a reason to stop. Stop for actual conflicts, diverged local `main`, missing refs, or uncertain ownership of changes.
- A successful fetch or push does not update the local checkout. Verify the final branch, ancestry, and working tree.

## 1. Inspect and fetch

Read applicable repository instructions and `.envrc`. Use the required direnv and hosting-account context for remote operations; stop if access is blocked. Verify repository identity without displaying credentials.

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short --branch
git config user.name
git config user.email
git remote -v
git fetch --prune origin
git show-ref --verify refs/heads/main
git show-ref --verify refs/remotes/origin/main
```

If either main ref is missing, ask which branch to use. Record the starting branch, HEAD, staged/unstaged diffs, untracked paths, and existing stashes. If another operation has left conflicts, resolve or report that state before starting another transition.

Inspect incoming work and overlap with local edits:

```bash
git log --oneline main..origin/main
git diff --name-status main...origin/main
git rev-list --left-right --count main...origin/main
```

If local `main` and `origin/main` have diverged, stop: reconciliation needs an explicitly agreed strategy. A fast-forward, equality, or local main already containing remote main can proceed without new commits.

## 2. Identify unpublished branch work

Skip this step when already on `main`, but still perform the remote update below.

For another starting branch, preserve its ref/HEAD and inspect commits relative to both main refs. If its HEAD is already an ancestor of `main` or `origin/main`, its committed work is already incorporated; do not replay it as local edits.

Otherwise identify only the branch work not already represented on the destination. Check patch-equivalent commits with `git cherry` as well as ancestry, especially after squash merges or cherry-picks. Save the remaining work as a binary-capable patch for restoration as working-tree changes, not new commits. Inspect and validate the patch against the updated destination before applying it. Do not blindly apply the whole merge-base-to-HEAD diff when some changes are already published; stop if the remaining delta cannot be isolated safely.

Completion: every starting-branch change is accounted for as already included, an unpublished patch, or an explicit blocker.

## 3. Preserve edits, then update main

When local changes exist, create a named stash including untracked files and record its exact object ID. Use that ID for restoration rather than assuming `stash@{0}` remains yours.

```bash
git stash push -u -m "back-to-main-preserve-local-work"
git rev-parse refs/stash
```

Only record a new stash ID if a stash was actually created. Verify the checkout is clean before switching/updating. If concurrent edits appear, stop rather than overwriting them.

Switch only if needed, then incorporate the fetched remote work:

```bash
git switch main                 # only when not already on main
git merge --ff-only origin/main
```

If remote main is already contained locally, the merge is a no-op. Otherwise this advances local main to include the published commits. Do not stop merely because the starting branch was already `main`.

Repository hooks may build before local edits are restored. If a hook fails, inspect HEAD and status: the fast-forward may already have succeeded. Report the build failure separately, and restore saved work before retrying builds. Do not blindly repeat the pull, bypass required hooks, or assume a failed command rolled back Git state.

## 4. Restore and verify local work

Apply any validated unpublished branch patch, then restore the recorded stash with `git stash apply --index <saved-stash-id>` so previously staged changes are preserved. Use `apply`, not `pop`, to retain recovery data until verification.

If patch application or stash restoration conflicts, keep the patch, original branch, and stash; inspect unmerged paths and report exactly what remains. Resolve only within the user's authorization, preserving both the incoming change and unrelated local work. Do not reapply a partially restored stash or equate an empty unmerged-path list with complete restoration.

Compare the final diff and untracked files with the preflight inventory. Every saved edit must be restored or demonstrably included in incoming commits. Drop only this operation's stash after that comparison succeeds; otherwise retain it and report its ID.

## Done criteria

```bash
git branch --show-current
git merge-base --is-ancestor origin/main HEAD
git diff --name-only --diff-filter=U
git status --short --branch
```

Finish only when:

- The current branch is `main` and contains the fetched `origin/main`.
- Requested published work is present in this checkout, not just on GitHub or in another worktree.
- Unpublished work is restored, with no unresolved conflicts or unexplained missing edits.

Report the incoming commits, preserved local work, retained recovery artifacts, and any blockers. If a rebuild or runtime verification was requested, do it after restoration and verify the active executable uses this checkout. Otherwise stop without committing, pushing, or running a full test suite.
