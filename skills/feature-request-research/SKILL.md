---
name: feature-request-research
description: Research an existing codebase, pull requests, issues, commits, and documentation before planning or implementing a feature request. Use when asked to investigate whether a feature request already exists, find prior attempts, identify related code paths, compare implementation options, or produce an evidence-backed recommendation before writing code.
---

# Feature Request Research

Use this skill to answer "what should we know before building this?" Ground every conclusion in repository evidence, issue/PR history, docs, tests, and the current code.

Do not implement code changes unless the user explicitly asks to move from research into implementation.

## Research Workflow

1. Capture the request in one or two sentences, including the user-visible behavior, affected product area, and any acceptance criteria.
2. Inspect repository basics:

```bash
git status --short
git branch --show-current
git remote -v
git log -5 --oneline
```

3. Search the codebase for domain terms, UI labels, routes, commands, API names, config keys, test names, and nearby concepts:

```bash
rg -n "term|related phrase|apiName" .
rg --files
```

4. Trace the most relevant implementation paths through callers, tests, fixtures, docs, public exports, route handlers, feature flags, generated files, and package boundaries.
5. If a GitHub remote and `gh` authentication are available, search existing and historical issue/PR evidence:

```bash
gh issue list --state all --search "terms from request" --limit 20
gh pr list --state all --search "terms from request" --limit 20
gh pr view <number> --comments --files
gh issue view <number> --comments
```

6. If `gh` is unavailable, unauthenticated, or the repository is not hosted on GitHub, continue with local git evidence and state the limitation briefly.
7. Review prior attempts or related changes with local history when useful:

```bash
git log --all --oneline -- "path/to/relevant/file"
git log --all --grep "term from request"
git blame -- "path/to/relevant/file"
```

## Analysis

Separate evidence from inference:

- Existing support: what already works, what is hidden behind flags/config, and what only needs exposure or wiring.
- Prior art: related PRs, issues, commits, reverted attempts, TODOs, docs promises, and test coverage.
- Affected surface: files, modules, owners, APIs, database/storage, background jobs, UI states, and migration risks.
- Constraints: compatibility, permissions, security/privacy, performance, rollout, release process, generated artifacts, and known flaky areas.
- Options: at least two plausible implementation approaches when the solution is not obvious, with tradeoffs.
- Unknowns: questions that genuinely block a confident recommendation.

## Output

Return a concise research brief with:

- Request summary.
- Evidence found, with file paths, PR/issue numbers, commit hashes, or commands used.
- Relevant code paths and tests to inspect first.
- Recommendation and why.
- Implementation outline only if enough evidence supports it.
- Risks, unknowns, and suggested verification.

Do not fabricate PRs, issues, links, owners, metrics, or behavior. If evidence is missing, say so plainly.
