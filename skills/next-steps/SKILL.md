---
name: next-steps
description: Continue from the next actionable step in the current conversation context. Use when the user asks to continue, go on, do the next step, resume from context, or finish previously identified follow-up work.
---

# Next Steps

Use this skill to continue active work from the conversation instead of restarting analysis or giving a generic list.

## Workflow

1. Identify the active objective from the latest user request and the recent conversation. Prefer explicit next steps, unchecked task-list items, blocked work that is now unblocked, or the last incomplete implementation or verification step.
2. Ignore stale suggestions that no longer match the user's latest request. If more than one next step exists, choose the step that unblocks the objective with the least unrelated scope.
3. Check local state before acting when the next step depends on files, commands, branches, servers, tests, or external tool state. Do not rely only on earlier conversation text when the current state is cheap to verify.
4. If the next step is actionable, do it. Avoid replying only with a plan unless the user explicitly asks for a plan or the step needs approval.
5. When the context is insufficient, ask one concise question only if a reasonable assumption would create a material risk. Otherwise state the assumption and proceed.
6. After completing a step, run the smallest useful verification. Then either continue to the next obvious step or report what remains.

## Selection Rules

- Latest user instruction wins over older task lists or assistant suggestions.
- Prefer finishing already-started work before adding new scope.
- Prefer verification after changes when no implementation step is clearly pending.
- Treat "next steps" as concrete work, not as a request for a broad roadmap, unless the user asks for a roadmap.
- Preserve normal authorization boundaries for side effects such as sending messages, publishing, deploying, buying, deleting, or changing remote production state.

## Output

Keep the response short and state:

- What next step was selected.
- What was done or why it is blocked.
- What verification was run.
- The next remaining step, if one is clear.
