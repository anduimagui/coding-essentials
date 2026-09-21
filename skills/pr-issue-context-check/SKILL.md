---
name: pr-issue-context-check
description: Search GitHub issues and pull requests to determine whether a feature, bug, or implementation is already in progress, discussed, shipped, rejected, or unresolved. Use when asked to check if anyone is working on something, find existing PRs or issues for a topic, understand the status of a GitHub conversation, determine if work has started on a feature, search for related discussions before opening a duplicate, or investigate who is tackling a particular problem. Trigger on phrases like "has anyone started", "is there already a PR", "who's working on", "find related work", or "search issues and PRs".
---

# PR / Issue Context Check

Search GitHub issues and pull requests to find existing work before duplicating effort. Look for explicit signals like assignees, draft PRs, WIP labels, and maintainer comments that indicate someone has already started.

Do not search the local codebase unless the user explicitly asks you to connect GitHub context back to implementation.

## Workflow

1. Parse the query into search terms. Extract the feature name, bug, component, and synonyms. Build both exact and fuzzy keyword lists. For "who's working on" queries, prioritize assigned items, draft PRs, WIP labels, and recent activity.

2. Identify the repository from `git remote get-url origin`. If ambiguous, check available remotes. If no repo can be inferred, ask for the GitHub URL.

3. Search PRs with `gh pr list --search "<keywords>"` across open, merged, and all states. For promising results, read the body and comments with `gh pr view <number>`. Capture number, title, URL, state, author, dates, labels, assignees, linked issues, and relevance.

4. Search issues with `gh issue list --search "<keywords>"` across open and all states. Read promising threads with `gh issue view <number>`. Capture number, title, URL, state, author, dates, labels, assignees, closing references, and maintainer guidance.

5. Cross-reference links between issues and PRs. Follow "duplicate of", "closes", and "fixed by" references to find canonical threads.

6. Consolidate and de-duplicate results. Keep borderline matches with an uncertainty note rather than dropping them.

7. Determine the conversation status using evidence:
   - `active_pr`: open PR with implementation work
   - `active_discussion`: open issue or PR thread deciding direction
   - `shipped`: merged PR or maintainer completion statement
   - `rejected_or_abandoned`: closed as not planned or stalled
   - `duplicate_or_superseded`: redirected to another canonical thread
   - `no_relevant_context_found`: no credible match found

8. Recommend where to participate next. Choose the single best open PR or issue when one exists. If nothing suitable exists, recommend opening a new issue or PR.

## Output

Return a report with the query, final status and confidence, evidence summary with counts, a table of PR incidents with links, a table of issue incidents with links, a timeline of major discussion points, any gaps or uncertainty, a recommended next action, and the single best place to contribute (or `None`).

Always include GitHub URLs for every incident. Do not claim something shipped without a merged PR or maintainer confirmation. When evidence is ambiguous, lower confidence and explain what is missing.
