---
name: straight-to-main
description: Publish a small, self-contained change directly to a repository's GitHub-defined default branch from a clean worktree. Use when a checkout has drifted onto another branch or contains unrelated local changes, but the requested change should be committed and pushed straight to the default branch after verifying direnv, Git identity, remote identity, and cleanup.
---

# Straight to Main

Use this skill when the requested change is small enough to publish directly to the repository default branch, but the current checkout is dirty, on the wrong branch, or carrying drift from previous work.

Do not assume the default branch is named `main`. Determine it from the remote hosting provider, preferably with GitHub CLI for GitHub repositories.

## Required Preflight

Before any command that changes history, reads or writes remotes, or depends on a hosting account:

1. Identify the active repository root with `git rev-parse --show-toplevel`.
2. Read the repository instructions, especially any `AGENTS.md` guidance for direnv, generated files, staging, and remote identity.
3. Check for an applicable `.envrc` in the repository root or parent path.
4. If `.envrc` exists and `direnv` is available, load it in the shell used for GitHub and git remote operations.
5. If direnv is blocked, stale, or not allowed, stop before remote or history-changing actions and ask the user how to proceed.
6. Verify local commit identity before acting:
   - `git config user.name`
   - `git config user.email`
   - `git remote -v`
7. For GitHub repositories, run the GitHub account access selection in this skill before the default-branch lookup, commit, pull, or push.
8. For non-GitHub repositories, verify the relevant hosting CLI account and continue only when the identity and remote match the intended repository account.
9. If the user's prompt names the GitHub account to use, capture that exact login as `TARGET_GITHUB_ACCOUNT` and treat the account switch or official web login as pre-authorized. Do not pause to ask whether to switch accounts, start login, or retry the direct push.

Never print secrets, tokens, private keys, or credential-helper output.

## Default Branch Discovery

For GitHub repositories, use the active repository identity to ask GitHub for the default branch:

```bash
gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
```

If the repository has a required direnv context for GitHub commands, run the query inside that context. For example:

```bash
direnv exec /path/to/repo gh repo view --json defaultBranchRef --jq .defaultBranchRef.name
```

If the hosting CLI cannot verify the default branch, stop before committing or pushing unless there is another authoritative repository source for the default branch.

## GitHub Account Access Selection

For GitHub repositories, do not trust the currently active `gh` account as proof that the push will work. Before any commit or push, find which locally authenticated GitHub accounts have direct write access to the target repository's default branch, usually `main`, select one, and make that account effective for all later GitHub and Git remote commands.

1. Resolve the repository name from the verified remote URL, then list locally logged-in GitHub accounts without printing tokens:

   ```bash
   gh auth status --hostname github.com
   gh auth switch --hostname github.com --user ACCOUNT_FROM_STATUS
   gh api user --jq .login
   ```

   Use `gh auth status --hostname github.com` as the account inventory. For each shown account, switch to that account and verify `gh api user --jq .login` returns the same login before testing access.

2. For each logged-in account, check repository permission and default branch in that account context:

   ```bash
   gh repo view OWNER/REPO --json viewerPermission,defaultBranchRef --jq '{permission: .viewerPermission, branch: .defaultBranchRef.name}'
   ```

   Treat `ADMIN`, `MAINTAIN`, and `WRITE` as candidate direct-push permissions. Treat `READ`, `TRIAGE`, missing repository access, and command failures as not sufficient.

3. If repository rules can block direct pushes, check branch protection or rulesets for the discovered default branch when the selected account can read them. If the rules show the account cannot push directly to the default branch, remove that account from the candidate list. If rules cannot be read, keep the account as a candidate but verify the effective account again before push and report any later GitHub rejection exactly.

4. Select the account:
   - If the user's prompt names a GitHub account, use only that account. Stop if it is not logged in, cannot be made effective, or lacks direct access to the default branch.
   - If exactly one logged-in account has direct access, switch to it and continue.
   - If more than one logged-in account has direct access, ask the user which account to use. Show only the login, permission, and default branch. Do not commit or push until the user chooses.
   - If no logged-in account has direct access, stop before committing or pushing and report the tested accounts and repository target.

5. After selection, make the selected account effective for all commands that read GitHub state or use GitHub credentials. Re-run these checks immediately before `git pull --rebase --autostash` and `git push`:

   ```bash
   gh auth switch --hostname github.com --user "$TARGET_GITHUB_ACCOUNT"
   test "$(gh api user --jq .login)" = "$TARGET_GITHUB_ACCOUNT"
   gh repo view OWNER/REPO --json viewerPermission,defaultBranchRef
   ```

6. Use a command-scoped account override if direnv or the repository environment pins another GitHub account. Do not edit tokens or print credential-helper output. Prefer making `gh auth switch` select the account, then run final Git transport commands in the same effective account context.

## Prompt-Specified GitHub Account

When the user's prompt specifies the GitHub account for the direct push:

1. Set `TARGET_GITHUB_ACCOUNT` to the exact login from the prompt. Require it to match GitHub's username characters (`A-Z`, `a-z`, `0-9`, and `-`); never interpolate arbitrary prompt text into a shell command.
2. Do not create a pull request or ask whether to switch accounts. Check whether the target account is already authenticated and switch to it before the first repository mutation:

   ```bash
   TARGET_GITHUB_ACCOUNT="account-from-user-prompt"
   gh auth status --hostname github.com
   gh auth switch --hostname github.com --user "$TARGET_GITHUB_ACCOUNT"
   gh api user --jq .login
   ```

3. If the target account is not authenticated, immediately start GitHub's official device login without asking first:

   ```bash
   gh auth login --hostname github.com --web --git-protocol https
   ```

   Share the one-time device code as a progress update, open the browser when prompted, wait for completion, and verify that `gh api user --jq .login` returns exactly `$TARGET_GITHUB_ACCOUNT`. Never discover, print, or rewrite tokens manually.

4. Set and re-read the repository-local commit identity before amending or creating the commit:

   ```bash
   git config user.name "$TARGET_GITHUB_ACCOUNT"
   git config user.email "${TARGET_GITHUB_ACCOUNT}@users.noreply.github.com"
   git config user.name
   git config user.email
   ```

5. If `.envrc` pins a different GitHub account through `GH_CONFIG_DIR` or `GTL_GITHUB_ACCOUNT`, keep using the required direnv context but override only those account selectors for GitHub and Git remote commands:

   ```bash
   direnv exec /path/to/repo \
     env -u GH_CONFIG_DIR GTL_GITHUB_ACCOUNT="$TARGET_GITHUB_ACCOUNT" \
     gh api user --jq .login
   ```

   Use the same `direnv exec ... env -u GH_CONFIG_DIR GTL_GITHUB_ACCOUNT="$TARGET_GITHUB_ACCOUNT"` prefix for the final pull and push. Verify the effective account exactly matches the requested login immediately before mutation.

6. Amend the local commit author if it was prepared under another account, re-run the relevant validation, then run `git pull --rebase --autostash` and perform the direct push.
7. If GitHub rejects the push because repository rules require a pull request, retry only after confirming the prompt-specified account is still effective and has the required bypass permission. Do not substitute a different account.
8. Stop only if device authorization fails, the effective account does not exactly match `TARGET_GITHUB_ACCOUNT`, or that account lacks permission. Report the exact blocker without falling back to a pull request.

If the prompt does not name an account, use the GitHub account access selection instead of the active account. Never invent a username or account fallback.

## Clean Worktree Path

Use a separate clean worktree when the current checkout has unrelated edits, is on a drifted branch, or has generated output that would mix with the requested change.

1. Confirm the current checkout's dirty state so unrelated edits are known and preserved.
2. Create a temporary worktree from the verified default branch.
3. Pull or fetch/rebase the temporary worktree so it is current with the remote default branch.
4. Apply only the requested small change in the temporary worktree.
5. Run the repository's required validation or build commands.
6. Inspect the diff and ensure only the requested source files and required generated follow-up files changed.
7. Stage explicit paths only; never use `git add .` or `git commit -a`.
8. Commit with the repository's existing message style.
9. Run `git pull --rebase --autostash`, then `git push`.
10. Check `git status --short --branch`.

When the temporary worktree lacks ignored local files such as `.envrc`, run hosting and push-sensitive commands through the original repository's direnv context, for example:

```bash
direnv exec /path/to/original/repo git -C /path/to/temp-worktree push
```

## Cleanup

After a successful push:

1. Remove only this session's duplicated change from the original dirty checkout, if it was first applied there.
2. Leave unrelated existing edits and untracked files untouched.
3. Remove the temporary worktree.
4. Re-check the original checkout status and confirm it no longer contains the just-published change.

Do not reset, checkout, or delete unrelated local work unless the user explicitly asks for that cleanup.

## Reporting

In the final response, include:

- The commit hash and message.
- The verified default branch name and how it was discovered.
- The files included in the commit.
- The validation/build command that passed.
- Whether the original drifted checkout was cleaned back to unrelated local changes only.
