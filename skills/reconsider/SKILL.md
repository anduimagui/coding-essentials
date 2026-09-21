---
name: reconsider
description: Rethink an existing proposal, plan, recommendation, architecture, message, or decision in light of extra context from the current session or newly provided by the user. Use when asked to reconsider, revisit, challenge, adjust, reverse, salvage, narrow, or reframe a specific idea after assumptions, constraints, evidence, priorities, stakeholders, or goals have changed.
---

# Reconsider

Use this skill to revisit a concrete idea without defending the original answer by default. Treat the new context as potentially decision-changing, then decide whether to keep, revise, replace, or discard the proposal.

## Workflow

1. Identify the original proposal precisely. Restate the decision, recommendation, plan, draft, or design being reconsidered in one sentence.
2. Extract the new context. Separate explicit new facts from inferred implications, and call out any missing context that would materially change the conclusion.
3. Rebuild the evaluation criteria from the user's current goal. Include constraints, risk tolerance, time pressure, audience, scope, reversibility, and success measures.
4. Compare the original proposal against the updated criteria. Identify what still holds, what breaks, what becomes less important, and what new option appears.
5. Decide the right disposition:
   - Keep: the proposal still fits; only explain why the new context does not change it.
   - Adjust: the core idea is sound but needs scoped changes.
   - Replace: a different approach now better satisfies the goal.
   - Defer: the context is insufficient and acting now would create avoidable risk.
6. Give the revised recommendation directly, then provide the reasoning needed to trust it. Avoid a long historical recap unless the user asks for it.
7. If implementation or writing changes are needed, apply the revised direction instead of only describing it when the user has asked for action.

## Reconsideration Checks

- Assumptions: Which old assumptions are now false, weaker, or unproven?
- Goal fit: Is the user still optimizing for the same outcome?
- Scope: Is the proposal too broad, too narrow, or aimed at the wrong layer?
- Evidence: Does the new context outweigh the old evidence, or merely add an edge case?
- Cost: What time, complexity, money, coordination, or maintenance cost changes?
- Risk: What failure modes, user impact, legal/security/privacy concerns, or reputational issues are newly visible?
- Reversibility: Can the choice be tried cheaply, or does it create lock-in?
- Stakeholders: Does the audience, buyer, reviewer, customer, or maintainer now require a different framing?

## Output

Lead with the updated recommendation. Use a compact structure:

- Original proposal: one sentence.
- New context that matters: short bullets.
- Decision: keep, adjust, replace, or defer.
- Revised proposal: concrete next version.
- Why: the decisive tradeoffs.
- Next action: the smallest practical step, if action is appropriate.

When the user asks for terse help, compress this into a short answer with the recommendation first.

## Guardrails

- Do not treat reconsideration as a debate exercise. Change the answer when the new context warrants it.
- Do not overfit to the latest detail if the broader goal is unchanged.
- Do not preserve the original proposal for politeness. Preserve it only when it remains the best fit.
- Do not ask for clarification when the available context supports a reasonable updated recommendation; state assumptions and proceed.
- Do not bury the new answer after a long explanation of the old one.
