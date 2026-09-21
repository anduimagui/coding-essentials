---
name: back-to-main
description: Move local work from the current branch back onto main while staying on main. Must detect upstream changes that may cause conflicts first. Must not create commits.
---

# Back to Main

Use this skill when you accidentally did work on a non-`main` branch and want to return to `main` **with all your local work preserved**, but **without committing anything**.

This skill:

- Checks whether `origin/main` has new commits that are not in your current branch (these may cause conflicts).
- If it looks risky, it **warns and stops** before changing anything.
- If it looks safe, it moves your work onto `main` as **working tree changes** (not commits) and stops as soon as you are back on `main`.

## Hard Rules

- **Do not make commits.**
- **Do not push.**
- **Do not rewrite history** (`reset --hard`, `rebase -i`, etc.).
- **Stop immediately** once we are on `main` and the local changes are present.

## Required Preflight

1. Identify repo root:

   ```bash
   git rev-parse --show-toplevel
   ```

2. Check current state:

   ```bash
   git branch --show-current
   git status --short --branch
   ```

3. Fetch remote refs:

   ```bash
   git fetch --prune origin
   ```

4. Confirm `main` exists locally and remotely:

   ```bash
   git show-ref --verify --quiet refs/heads/main
   git show-ref --verify --quiet refs/remotes/origin/main
   ```

   If either ref is missing, stop and ask the user what the default branch is.

## Detect Remote Changes That May Cause Conflicts

We want to know if `origin/main` moved ahead since this branch diverged.

1. Find the merge-base between the current `HEAD` and `origin/main`, then count remote commits beyond it:

   ```bash
   BASE_REMOTE=$(git merge-base HEAD origin/main)
   REMOTE_AHEAD=$(git rev-list --count "$BASE_REMOTE"..origin/main)
   echo "REMOTE_AHEAD=$REMOTE_AHEAD"
   ```

2. If `REMOTE_AHEAD` is **greater than 0**:

   - Warn the user: "`origin/main` has new commits not in this branch; moving changes back to main may conflict."
   - Show the commit summary:

     ```bash
     git log --oneline --decorate -n 20 "$BASE_REMOTE"..origin/main
     ```

   - **Stop**. Do not switch branches, stash, apply patches, or modify files.

If `REMOTE_AHEAD=0`, proceed.

## Move Work Back Onto `main` (No Commits)

We will convert the branch's committed work into a patch, switch to `main`, apply the patch, then restore any uncommitted/untracked work.

1. Record the current branch name:

   ```bash
   CURRENT_BRANCH=$(git branch --show-current)
   ```

   If `CURRENT_BRANCH` is already `main`, stop (nothing to do).

2. Create a patch representing the branch's committed work relative to `main`:

   ```bash
   BASE_LOCAL=$(git merge-base HEAD main)
   PATCH_FILE=$(mktemp -t back-to-main.XXXXXX.patch)
   git diff "$BASE_LOCAL"..HEAD > "$PATCH_FILE"
   wc -l "$PATCH_FILE"
   ```

   Note: this patch only covers committed differences. Uncommitted changes and untracked files are handled by stashing in the next step.

3. If there are local uncommitted or untracked changes, stash them (no commits):

   ```bash
   if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
     git stash push -u -m "back-to-main-autostash"
     STASHED=1
   else
     STASHED=0
   fi
   ```

4. Switch to `main`:

   ```bash
   git switch main
   git status --short --branch
   ```

5. Apply the committed-work patch (if it has content):

   ```bash
   if [ -s "$PATCH_FILE" ]; then
     git apply "$PATCH_FILE"
   fi
   ```

   If `git apply` fails, **stop** and report the failing files/hunks. Do not attempt a manual conflict resolution unless the user explicitly asks.

6. Restore stashed changes (if we stashed):

   ```bash
   if [ "$STASHED" = "1" ]; then
     git stash pop
   fi
   ```

   If `stash pop` reports conflicts, **stop** and report the conflicted files.

7. Confirm we are on `main` and the changes are present:

   ```bash
   git branch --show-current
   git status --short --branch
   ```

## Done Criteria (Stop Point)

Stop as soon as:

- `git branch --show-current` returns `main`, and
- `git status --short` shows the expected local changes.

Do not proceed to committing, pushing, or running a full test suite unless the user explicitly asks.
