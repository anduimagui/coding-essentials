---
name: implementation-compare
description: Inspect existing code and context, then produce a durable visual-first comparison of alternative ways to implement a feature, user flow, pipeline, CI/CD flow, data flow, or infrastructure topology. Create a linked Markdown report and a real visual when interaction or spatial layout matters. Use when asked to weigh or compare implementation approaches; not for single-solution design or plain code review.
---

# Implementation Compare

Compare a small number of credible ways to implement a plan and let one visual carry the comparison. End with one recommendation and show rejected options fairly. Save the comparison so the user can open it again and sync it with the project.

## Workflow

1. **Inspect first.** Read the relevant code, configs (CI, deploy, IaC, pipeline YAML), and docs before comparing. Determine what is fixed (existing services, storage, conventions) versus flexible, and locate where the options actually diverge. Tie every option to real code rather than an abstract strawman.

2. **Enumerate 2–3 options.** Each is a distinct, credible approach, not a cosmetic variant. Name them consistently (e.g., "A — Single job", "B — Queued workers").

3. **Model each option on the same dimensions** so alternatives are directly comparable:
   - Components and deployment units (services, jobs, storage, caches, queues)
   - Data flow and control flow (who calls whom; sync vs async)
   - Boundaries (API, module, event, or DB seams)
   - Queues, retries, idempotency, backpressure
   - Failure paths and recovery (what breaks, how it degrades, blast radius)
   - Operational burden (new workers, relays, crons, queues, datastores, control planes, secrets, monitors, runbooks, deploy targets)
   - Tradeoffs: cost, latency, security, complexity

   A dimension handled differently by current code is a fact; an inferred cost or latency number is an assumption. Never invent numeric scores, ratings, or stars.

4. **Gate on hard constraints.** Extract explicit hard constraints — requirement wording such as "must", "cannot", "not acceptable", plus compliance or security limits — and treat them as a pass/fail gate for every option before weighing tradeoffs. Do not turn an ambiguity into a convenient assumption when it changes which option wins. If a missing fact or ambiguity changes whether an option passes a hard constraint, no option is valid yet — never issue a conditional recommendation past an unresolved hard-constraint gate.

5. **Produce the visual.** Create the visual. Do not only describe what a future visual can show.

   - Default to Mermaid when labeled nodes and edges fully explain a static implementation. Pick the diagram shape from [references/mermaid-guide.md](references/mermaid-guide.md).
   - Use HTML when the user must compare interaction states, edit a graph, draw connections, switch between options, or inspect a spatial user flow. Follow [references/html-visualization.md](references/html-visualization.md) and the active visualization capability.
   - When the user requests several visual concepts, create each requested concept. One HTML file with clear tabs is acceptable when it keeps the comparison compact.
   - Mark options that fail a hard constraint with the literal label `INVALID` plus the failed constraint. Mark the winner with the literal label `RECOMMENDED`. Show the deciding constraint and each option's main failure or recovery path.

6. **Connect the implementation to the user flow.** State how the user reaches, changes, saves, syncs, and consumes the result. Name the primary product surface and any companion surface. Distinguish these parts:

   - Web or application dashboard
   - CLI or local agent path
   - Local and cloud storage
   - Sync or cache path
   - Final consumer, such as generated context, an API, or an LLM

   Do not make manual JSON editing the normal user flow. Treat JSON, databases, and cache files as implementation details unless the user explicitly asks for a file-editing workflow. Mark proposed commands and APIs as proposed. Do not present them as current features.

7. **Save linked artifacts together.** Write the full comparison to a Markdown file. Put the Markdown file and any HTML visual in the same durable project folder when possible.

   - Use a folder that the user specifies.
   - If the user requests sync but gives no folder, use a tracked project documentation folder such as `docs/proposals/`.
   - If the content must stay local, use a gitignored project folder instead.
   - Do not leave the only HTML copy in an ephemeral or tool-owned visualization folder when the user requests a durable or synced result.
   - Link from the Markdown file to each HTML visual with a relative path.
   - Preserve unrelated worktree changes. Do not commit or push unless the user asks.

8. **Verify and recommend.** Verify that each requested visual exists, each Markdown link resolves, and interactive controls work at normal and narrow widths. Confirm that durable artifacts are inside the intended tracked or ignored folder. Then recommend. Never recommend an option that violates a hard constraint; existing dependencies and low operational cost are tie-breakers only among options that pass the gate. If no option is known to satisfy every hard constraint, lead with "No valid recommendation yet" and state the smallest missing fact, scope clarification, or additional option needed — do not pick a lesser evil. Prefer existing dependencies and architecture. If every hard constraint is proven to pass, a missing tie-breaker may make the recommendation conditional; name that missing fact.

## Output shape (in this order)

1. One-line conclusion — the recommendation, or "No valid recommendation yet" naming the blocker.
2. One short context sentence: what is fixed and what the decision hinges on.
3. The visual as the centerpiece. Embed Mermaid in the report, or link a real HTML visual from the report.
4. The end-to-end user flow: entry surface, edit action, persistence, sync, and final consumer.
5. Winner reasons — at most 2 short reasons — then rejected options with at most 1 short loss reason each. If no option passes the gate, give the blocker and missing facts instead.
6. A brief "Facts vs assumptions" list.
7. Clickable paths to the Markdown report and each durable HTML visual.

Do not add a prose table that repeats the visual.

## Rules

- Use 2–3 options by default. If the user requests an exact number, create that number and keep the comparison dimensions consistent.
- Create at least one directly comparable visual. Prose is annotation only.
- A written description of a graph is not a visual graph. Create the Mermaid or HTML content and verify it.
- The Markdown report is the index for the work. Keep visual links relative so the report works after clone or sync.
- Use the same dimensions for every option so differences can be eyeballed.
- No invented numbers, scores, or ratings. Mark unknowns explicitly or say where to measure.
- Distinguish fact (from inspected code) from assumption (inferred) inline or in the facts list.
- Count every new worker, relay, cron, queue, datastore, control plane, secret, monitor, runbook, and deployment target as operational change. Do not claim a seam or unit is unchanged if any contract, behavior, process, or ownership changes.
- Absence from the inspected scope is "not observed", not proof that something does not exist.
- A requirement target (e.g., "2 seconds") is a constraint, not proof the design meets it. Mark predicted compliance as an assumption until measured.
- Do not turn an ambiguity into a convenient assumption when it changes which option wins.
- If a missing fact or ambiguity changes whether an option passes a hard constraint, no option is valid yet. Conditional recommendations are not allowed for unresolved hard-constraint gates. Lead with exactly "No valid recommendation yet".
- Self-audit the visual before final output: a `RECOMMENDED` option must have no shown failure path, assumption, or unknown that can violate a hard constraint. If it does, remove `RECOMMENDED`, mark the option `INVALID` or `UNPROVEN` with the affected constraint, and use "No valid recommendation yet".
- A conditional recommendation is allowed only when every hard constraint is already proven to pass and the unknown affects only a tie-breaker.
- Do not infer a failure outcome from one config flag alone unless the outcome is observed or sourced; mark it as an assumption.
- Do not state likelihood, frequency, performance, or reliability claims as facts unless observed in inspected evidence or supported by a source; mark them as assumptions.
- Keep normal prose compact — about 350 words or less unless the user asks for detail.

## References

- [references/mermaid-guide.md](references/mermaid-guide.md) — diagram idioms per scenario.
- [references/html-visualization.md](references/html-visualization.md) — when an inline (non-Mermaid) visualization is warranted and how to contract it.
