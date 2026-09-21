---
name: propose-enhancements
description: Suggest improvements for the current product, feature, workflow, configuration, prototype, or software implementation based on the active conversation and available project context. Use this skill when the user says "suggest improvements", "suggest improvement", "how can we improve this", "what should we improve", asks what else should be added, asks what parameters or controls are missing, asks how the current setup should evolve, or wants product and technical improvement ideas grounded in work already underway.
---

# Propose Enhancements

Turn the current discussion and artifacts into a small, concrete set of useful product and technical improvement suggestions. Think one stage ahead of the present implementation while staying grounded in demonstrated needs.

## Build the Current-State Model

1. Review the conversation, relevant files, configuration, tests, and recent changes available in the current task.
2. State briefly what exists now, what problem it solves, and any constraints or decisions already established.
3. Separate verified behavior from assumptions. Inspect available evidence before asking the user for context that can be discovered.
4. Identify the newly introduced concept that may expose a broader design axis. For example, replacing a boolean recursive-folder option with `folderDepth` reveals related needs around scope, filtering, discoverability, exclusions, and previewing results.

Do not re-propose features that are already implemented unless suggesting a specific extension or correction.

## Explore the Next Usage Stage

Test the current setup mentally against realistic changes in use:

- more items, users, repositories, folders, environments, or data;
- deeper or irregular structures;
- selective inclusion and exclusion;
- different defaults at global, project, and nested scopes;
- discoverability for someone who did not build the feature;
- inspection, debugging, and safe preview before applying a setting;
- automation and non-interactive use;
- performance, ambiguity, invalid input, and conflicting configuration.

Treat this as a prompt for context-specific reasoning, not a checklist that must produce a proposal in every category.

## Form Concrete Enhancements

For each promising enhancement:

1. Name the user problem or friction first.
2. Describe the proposed behavior precisely.
3. Give at least one specific scenario in which it matters.
4. When relevant, propose the user-facing parameter, command, configuration shape, or interaction. Include example values and define their semantics.
5. Explain how it composes with the current setup, including precedence, defaults, boundaries, and invalid combinations where those details matter.
6. Identify the smallest end-to-end version that delivers value.
7. Include priority, effort, impact, and a concise acceptance check so the idea is testable.

Look especially for a general parameter hidden behind a one-off request. Prefer bounded, composable controls over accumulating narrowly named booleans when the underlying concept is a scale, mode, scope, or policy.

Include both product improvements and technical improvements when both are useful. Do not force balance if the context clearly supports one side more strongly than the other.

## Prioritize

Rank proposals using evidence from the current work:

- **Now:** removes demonstrated friction or completes the newly added capability.
- **Next:** likely to become important in the next realistic usage stage.
- **Later:** plausible but dependent on scale or behavior not yet observed.

Recommend up to five strong improvements by default. It is acceptable to return one, two, or three suggestions when only that many are well supported. Never pad the answer with weak ideas to reach five. Avoid an exhaustive feature wishlist. Flag proposals that add disproportionate configuration or conceptual complexity.

## Output Format

Lead with a one-paragraph assessment of the current setup and the most important next move. Then present each enhancement with:

- **Enhancement:** concise title.
- **Type:** Product, Technical, or Both.
- **Priority:** Now, Next, or Later.
- **Effort:** Small, Medium, or Large.
- **Impact:** Low, Medium, or High.
- **Problem:** the concrete limitation.
- **Proposal:** exact behavior or interface.
- **Scenario:** a realistic example.
- **Smallest useful version:** the minimal coherent implementation.
- **Acceptance check:** observable proof it works.
- **Tradeoff:** only when material.

End with a recommended sequence when proposals depend on one another. If there is only one compelling enhancement, say so rather than padding the answer.

## Guardrails

- Stay consistent with existing architecture and terminology unless changing them is itself the proposal.
- Prefer extending an established configuration model over creating a parallel mechanism.
- Do not preserve obsolete paths merely for compatibility; propose the clean current model.
- Distinguish product enhancements from implementation refactors.
- Do not implement proposals unless the user also asks for implementation.
- Ask a question only when a missing product decision would materially change the recommendations and cannot be inferred from available context.
