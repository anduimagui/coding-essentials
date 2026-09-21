---
name: cli-guider
description: Guide users through CLI setup, login, reauthentication, and secret-entry flows without running interactive credential prompts inside the agent terminal.
---

# CLI Guider

Use this skill when a task needs a CLI setup flow that can become interactive, especially authentication, reauthentication, password entry, browser login, device-code login, MFA, keychain access, account selection, token creation, or secret entry.

## Core Rule

Do not start a command in the agent terminal if it can ask the user for a password, passphrase, MFA code, browser login, device code, keychain unlock, SSH key unlock, personal access token, OAuth consent, or other secret.

Instead, give the user the exact command to run in their own terminal and ask them to paste back only the non-secret result that proves success or failure.

## What The Agent Can Run

The agent can run non-interactive checks that do not request secrets, such as:

- CLI version checks.
- Current configuration reads.
- Auth status checks that fail cleanly without prompting.
- Token checks that redirect token output away from chat and only report success or failure.
- Project, account, and permission reads after the user confirms authentication.

Use flags and environment settings that prevent prompts when the CLI supports them. If a command unexpectedly prompts, stop it and switch to user-run instructions.

## What The User Must Run

Give the user commands to run locally for:

- Login or reauthentication commands.
- Commands that open a browser login flow.
- Commands that ask for a device code, password, passphrase, MFA code, or keychain password.
- Commands that create or paste secrets, tokens, or credentials.
- Commands where a failed auth state can turn a normal read command into an interactive prompt.

Tell the user not to paste secrets into chat. Ask for status lines, account names, command exit results, or redacted output only.

## User Instruction Pattern

When handing off a command, be explicit and concise:

```text
Please run this in your terminal:

<command>

Do not paste any password, token, MFA code, or browser code here. When it finishes, paste the success or error text that does not contain secrets.
```

If the command prints a token or secret, add a redirection or a safer verification command so the user does not need to expose it.

## Verification Pattern

After the user reports that authentication is complete, run only verification commands that avoid printing credentials. Good examples:

```bash
gcloud auth list --format='table(account,status)'
gcloud config list --format='text(core.account,core.project)'
gcloud auth print-access-token >/tmp/gcloud-token-check 2>/tmp/gcloud-token-error && echo token_ok || { echo token_failed; sed -n '1,80p' /tmp/gcloud-token-error; }
```

Adapt the commands to the CLI in use, but keep the same rule: verify capability without printing secrets.

## Failure Handling

If authentication is still not ready, do not retry the interactive command from the agent terminal. Give the user the next command to run, explain what non-secret output to return, and wait.

If a previously started command is waiting for a secret in the agent terminal, stop it before continuing. Report that the auth flow must be completed by the user in their own terminal.
