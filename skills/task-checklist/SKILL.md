---
name: task-checklist
description: Keep an in-session checklist of tasks previously proposed by the assistant, preserving completed and pending state across follow-up work. Use when the assistant recommends multiple actions, the user asks to do one item first, asks what remains, or risks losing track of suggested next steps after completing a specific task.
---

# Task Checklist

Use this skill to keep proposed work visible while a conversation narrows to one task. Return the current checklist with checked or unchecked marks and recommend one next item.

## Workflow

1. Capture each concrete task the assistant proposed, including tasks from earlier turns in the same session, so prior suggestions do not disappear.
2. Normalize duplicates into one concise task while preserving user wording when it identifies a specific action.
3. Mark an item complete only when it was actually handled in the current session or the user explicitly says it is done.
4. When the user asks to work on one item first, complete that item if possible, then restate the full checklist immediately afterward.
5. Keep the checklist in session context. Do not create durable todo files unless the user explicitly asks for durable tracking.
6. Add new tasks when the assistant proposes them or the user adds them; remove tasks only when the user cancels them or they are clearly replaced.

## Recommendation

Recommend exactly one next task unless the user asks for prioritization. Choose by applying these priorities in order:

1. The user-specified next task.
2. A dependency that unblocks other pending tasks.
3. The highest-risk or most time-sensitive task.
4. The smallest verification step that proves recent work.
5. The shortest remaining task when all else is equal.

Give one short reason for the recommendation.

## Output

Include a compact checklist near the end of the response unless the user explicitly asks for only machine-readable output, a commit message, or a pull request message.

Use Markdown task-list syntax:

```markdown
**Task Checklist**
- [x] Completed task
- [ ] Pending task

Recommended next: Pending task, because short reason.
```

If a task was attempted but blocked, keep it unchecked and add a short blocker note in the task text. If no task has been completed, still show the proposed tasks with unchecked marks.
