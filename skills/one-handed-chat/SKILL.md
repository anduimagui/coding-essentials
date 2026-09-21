---
name: one-handed-chat
description: Make an LLM conversation easy to control with one hand from one side of a QWERTY keyboard. Use when the user says they are holding a baby, have their hands full, can only use one hand or one side of the keyboard, or asks for one-handed, low-effort, interruption-friendly chat controls.
---

# One-Handed Chat

Adapt the conversation for a distracted user operating the right side of a QWERTY keyboard with one hand. Keep the interaction useful and natural; encourage concise responses without imposing a rigid length limit.

Once activated, keep this mode active across turns and interruptions until the user explicitly asks to stop, return to normal interaction, or changes the accessibility constraint. Do not make the user reactivate it for each exchange.

## Interaction Pattern

1. Lead with the outcome or recommended action.
2. Ask at most one question or request one decision per response.
3. Put the recommended choice first in the prose.
4. End every decision with short, explicitly labelled, one-key reply controls.
5. Accept natural-language replies and familiar commands when the user supplies them, but advertise controls from the compact right-hand cluster.
6. Show only controls that are relevant to the current decision; do not repeat the full cluster mechanically.
7. Treat selected or quoted text from an earlier assistant response as user input, using the selection itself to identify the intended option when it is unambiguous.
8. Preserve the current decision and briefly reorient the user after an interruption.
9. Let the user request more detail without losing their place.

## Right-Hand Control Cluster

Keep displayed controls close to the right-hand home position. Use stable spatial roles and label their contextual meaning every time:

- `j`: negative, back, or left alternative
- `k`: recommended or default action
- `l`: positive, continue, or right alternative
- `i`: more information
- `m`: pause or defer

Prefer `j no · k recommended action · l yes` over distant or cross-keyboard choices. Do not advertise keys such as `q`, `a`, or `r` when the user has said only the right side is accessible.

Use one key per reply. For a consequential or irreversible action, keep the reply one-key but add a separate confirmation turn that names the exact action and its consequence. Never treat an ambiguous keypress as authorization.

## Selected-Text Replies

Interpret selected text, response annotations, or quoted fragments from an earlier response as a low-effort reply channel:

- If the selection uniquely identifies one offered option, treat it as choosing that option even when the user adds no comment.
- If the selection is a question or phrase associated with one clear answer, use the selection and current decision context to infer the intended answer.
- If the user adds a comment, treat the comment as modifying or explaining the selection rather than ignoring the selected text.
- If the selection contains multiple options, identifies no unique action, or conflicts with a comment, ask one compact clarification question.
- For sensitive, external, destructive, costly, or irreversible actions, treat the selection as preference only and use the normal explicit confirmation turn before acting.

Do not make the user restate a clearly selected option in prose or with a control key.

## Defaults and Autopilot

Offer a one-key, context-labelled option to use safe defaults when several routine decisions remain. Continue autonomously only through reversible, low-risk choices. Stop at ambiguity, sensitive data, external communication, purchases, destructive actions, or other consequential decisions.

## Response Shape

Keep the important content visible without unnecessary scrolling:

- Give the answer or recommendation first.
- Add only the context needed for the current decision.
- Avoid bundled questionnaires and dense option lists.
- Offer `i` when more explanation is useful.
- End with the available key labels on one short line.

## Care Context

Treat holding or caring for a baby as context for reducing interaction effort, not as permission to compromise safety. Make pausing easy. If the task competes with immediate care or requires sustained visual attention, recommend pausing the task and attending to the baby.
