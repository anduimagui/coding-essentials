---
name: explainer
description: Explain the current task, workflow, or process in simple, user-friendly language. Use when the user asks what Codex is doing, how the current process works, why a step is needed, what has happened so far, what will happen next, or for a plain-English status explanation without unnecessary technical detail.
---

# Explainer

Explain the work at the user's level so they can understand the goal, current
state, and next step without needing specialist knowledge.

## Workflow

1. Identify the process the user means from the active conversation and current
   task state.
2. State the goal in one short sentence.
3. Describe the process as a small number of concrete steps in the order they
   happen.
4. Clearly distinguish what is complete, what is happening now, and what remains.
5. Explain why a step matters only when that helps the user make sense of it.
6. Mention decisions, risks, blockers, or required user input when they affect
   the outcome.
7. End with the immediate next step or the finished result.

## Writing Rules

- Use plain language and short sentences.
- Lead with the outcome or purpose.
- Prefer familiar words over tool names, commands, and implementation details.
- Define any unavoidable technical term in the same sentence.
- Keep simple processes to a short paragraph or three to five steps.
- Use an analogy only when it makes the process easier to understand.
- Describe the actual current state. Do not present planned work as completed.
- Do not invent reasons, progress, timing, or results.
- Do not expose secrets, private data, hidden reasoning, credentials, or
  unnecessary internal details.
- Match the user's requested depth. If none is stated, give the shortest
  explanation that preserves the important context.

## Default Shape

Use this structure when it helps:

```markdown
The goal is [plain-English outcome].

So far, [completed work].

Right now, [current step and why it matters].

Next, [immediate next step or remaining work].

You need to [required decision or action, only if applicable].
```
