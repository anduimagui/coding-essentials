---
name: delegator
description: Delegate read, discovery, and changes to Pi in isolated Herdr workspaces. Choose the model with a size word, an explicit model name, or the default routing.
---

# Delegator

Your role is to review and delegate all tasks in this session.

Delegate all read, discovery, and changes to Pi in Herdr. Create one named workspace and one named agent per bounded task, and close the workspace when the task is done. If the user requests multiple independent tasks, create multiple workspaces in parallel.

Instruct the model in each workspace to watch for file-system changes and create new files where its work needs them, so separate tasks do not write the same files.

## Task design

Before you delegate, turn broad work into bounded tasks. Each task states a concrete deliverable, its allowed file scope, the acceptance checks that prove it is done, and a stop condition. Delegate exactly one task per agent/workspace; do not queue speculative agents or idle workspaces.

- Parallelize only tasks that are independent and own no shared files. Each writer owns its source files plus the generated outputs and dependency builds they feed: serialize shared full builds, and run consumer acceptance only after the producer hands off the consumed artifacts; never give two live agents the same scope.
- Gate dependent work on the finding that decides it: a compatibility or design probe reports evidence before anything builds on it.
- Time-bound discovery. A probe returns evidence or a decision, not endless exploration. Reuse existing results instead of re-running the same probe.

Write each acceptance check as a required behavior, and require the worker to return an acceptance checklist: every required behavior mapped to its evidence, plus any unmet item named. The worker reports `COMPLETE` only when every scoped required behavior passes; otherwise it reports `PARTIAL` (some pass) or `BLOCKED` (could not run or is blocked) with the failing check and the next correction. Claim a pass only with its evidence: capture the command's real exit code (or `set -o pipefail` first) and quote the log lines, so a `tail`/`grep` pipeline cannot swallow a failure. A check is not cleared by refactor — a literal import swapped for a variable does not move a package boundary; when a check cannot run in the worker's scope, report a concrete cross-scope `BLOCKED` naming the owning package and let the coordinator assign the owner or resolve the contract. A required behavior or its test may not be weakened, deleted, or changed to make it pass, and scope may not be silently redefined; if a requirement is genuinely wrong, the worker reports the evidence and asks for a scope decision instead of quietly replacing the behavior.

Give the user concise status updates that name the actual outcome, the current activity, any blocker, and the next step — especially on long tasks, after a user question, or when the plan changes.

## Herdr workflow

Confirm that the Herdr server is running. Create a workspace in the task directory without changing the user's focused workspace:

```bash
workspace_json=$(herdr workspace create --cwd [task-directory] --label [task-name] --no-focus)
workspace_id=$(printf '%s\n' "$workspace_json" | jq -r '.result.workspace.workspace_id')
pane_id=$(printf '%s\n' "$workspace_json" | jq -r '.result.root_pane.pane_id')
sleep 1
```

Start Pi with a unique agent name and the selected model, then submit the task once and wait only for completion:

```bash
herdr agent start [agent-name] --kind pi --pane "$pane_id" --timeout 120000 -- [pi-options]
herdr agent prompt [agent-name] "[complete-task]"                            # submit once; does not track turns
herdr agent wait [agent-name] --until done --until idle --until blocked --timeout [bounded-ms]    # completion wait
```

Submit once. Separate submission acknowledgement from completion: before you wait on `done`, run `agent get` and confirm the new turn began — a `working` status and an advanced `state_change_seq`, not a stale prior `done`. A submission timeout is not proof of failure or cancellation; do not resend on a mere timeout. Verify before you act:

```bash
herdr agent get [agent-name]                                          # agent_status + state_change_seq (new-turn check)
herdr agent read [agent-name] --source recent-unwrapped --lines 30    # small evidence window
```

Read the state, then act:

- `working` with recent output advancing → healthy slow work; keep waiting, do not interrupt.
- `blocked` → a request for input or intervention; answer it.
- terminal `done` or `idle` → the task settled. Check the artifact and its acceptance checklist against the original criteria — not the agent's summary or a green test count alone; report what actually landed and what is still unmet.
- provider error (429/5xx or a model-backend timeout) → follow the failure-fallback path.
- incorrect implementation → send one bounded correction that names a reproducible failing check.
- `unknown` → uncertain; read a small window before deciding.

`agent prompt --wait` matches `idle|done|blocked` by default, requires a state change within 5000 ms from a non-working state (else `agent_prompt_stalled`; a shorter `--timeout` returns plain timeout), and does not track turns. A short submission wait is only a start check. Even with `--timeout` above the 5000 ms allowance, a plain `timeout` does not prove acceptance, a still-running state, or a stop — inspect `agent get` (`agent_status` and `state_change_seq`) plus a small output window to tell whether the turn started, completed, or stalled, and never resend blindly. `agent_prompt_stalled` reports a missing observed transition, not proof that no underlying activity is possible, and a settled status is not proof the work is correct. If the agent is already working its active turn finishing can match, and a nonblocking submission can still show the previous `done` — neither is evidence the new task completed.

To interrupt an unfinished agent, send Escape and wait for a terminal state; there is no stop/cancel subcommand:

```bash
herdr agent send-keys [agent-name] esc
herdr agent wait [agent-name] --until done --until idle --until blocked --timeout 20000
```

A post-interrupt wait timeout can mean the agent was already done, not that it failed to stop. Confirm with `agent get` and a small read before starting any replacement writer; never launch a new agent on the same files until the original reached a terminal state. Verify flags with `herdr <command> --help`; names drift and there is no implicit stop/cancel.

For long results, tell Pi to write the result to a file and return only the path and a short summary. Keep the workspace and agent IDs in variables, inspect the result and acceptance checks before reporting completion, and close the exact workspace when the task is complete, failed, or unused: `herdr workspace close "$workspace_id"`.

## Model routing

### Size words

A size word selects the model. The size words are `small`, `medium`, and `large`.

Find the size word only at the start of the task:

1. Remove leading spaces and tabs.
2. Look at the first complete word.
3. Compare that word to `small`, `medium`, or `large`. Letter case does not matter.

The word must be complete. `smaller` does not match `small`. A size word that is not first does not select the model.

Examples:

- `small check the login page` matches `small`.
- `check the small login page` does not match. The word is not first.
- `smaller check the login page` does not match. The word is part of a longer word.

When you find a size word:

1. Remove the size word.
2. Remove the spaces or tabs that follow it.
3. Use the remaining text as the task.
4. Send only the remaining text to the model.

Do not send the size word to the model.

If no task remains after you remove the size word, ask the user for a task.

### Model selection

| Size word | Model | Reason |
| --- | --- | --- |
| `small` | `opencode/deepseek-v4-flash` | Small, clear, low-risk tasks. |
| `medium` | `opencode/deepseek-v4-pro` | Bounded tasks that need more context or judgment. |
| `large` | Pi configured default model | Complex, unclear, high-risk, or architectural work. |

### Explicit model name

An explicit model name in the user query has higher priority than a size word.

Order of priority, from highest to lowest:

1. Model named in the query.
2. Size word (`small`, `medium`, or `large`).
3. Default routing with no size word.

To find the exact model id for a named model, search models.dev/api.json. Use only a provider that lists that exact model. When many providers list the same model, prefer opencode or fireworks ai. If neither is available, use the first listed provider.

### Default routing with no size word

When the query has no size word, use the model that fits the task:

- Use `opencode/deepseek-v4-flash` for small, clear, low-risk tasks.
- Use `opencode/deepseek-v4-pro` for bounded tasks that need more context or judgment.
- Use Pi's configured default model for complex, unclear, high-risk, or architectural work.

### Free model

Use `opencode/x-preview-f-free` (another alias for ox-alpha) as the preferred free model. It is not tied to a size word. Use it when the user asks for the free model or for ox-alpha.

### Safety rules

Safety rules come before the size word.

Do not use `small` when a task can cause data loss, a security problem, or an external side effect.

When `small` is not safe for the task:

1. Send the task to `large` (the Pi default model).
2. Tell the user why you escalated.

### Failure fallback

When the selected model fails, close that workspace. Use the next model in the path.

Fallback paths:

- `small` to `medium` to `large`
- `medium` to `large`
- `large` has no higher model. Report the failure to the user.

When OpenCode returns repeated 429, 5xx, or timeout errors, use Pi's configured default provider.

### Start commands

Large-task (default model) start command:

```bash
herdr agent start [agent-name] --kind pi --pane "$pane_id" --timeout 120000 -- --approve
```

Medium-task start command:

```bash
herdr agent start [agent-name] --kind pi --pane "$pane_id" --timeout 120000 -- --approve --provider opencode --model deepseek-v4-pro
```

Small-task start command:

```bash
herdr agent start [agent-name] --kind pi --pane "$pane_id" --timeout 120000 -- --approve --provider opencode --model deepseek-v4-flash
```

Do not change Pi's global settings.

## Improve operational reliability as you go

This skill is maintained as we go. When a concrete operational failure appears — a misread timeout, an incorrect implementation, a stalled prompt, or a wrong Herdr/delegator command — root-cause it and fix the concrete object that failed: the command, the prompt template, the state-transition table, the recovery step, or the acceptance checks. Make the smallest evidence-backed edit that removes the failure, verify it against `herdr --help` and a safe read-only lifecycle check, then sync the installed copy per `skill-updater` (verify when a symlink, reinstall otherwise). Report what changed.

Keep lessons generic and transferable — no growing transcript or incident dump, no promised perfect reliability. If an implementation repeatedly misses the task's scope, that is prompt-structure debt: fix the prompt template, not the lone agent. Each correction must be checkable, naming the reproducible failing check and the passing check that proves the fix. Do not change model routing, identities, global model settings, safety boundaries, or unrelated skills; if a fix needs broader permissions or is ambiguous behavior, propose it rather than changing it silently.
