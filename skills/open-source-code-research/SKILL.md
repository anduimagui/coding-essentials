---
name: open-source-code-research
description: Find specific code examples in open-source GitHub, GitLab, or other public repositories for technologies the user needs to research. Use when asked to locate real repository implementations, compare open-source examples, inspect README claims, verify technology usage from code, or produce research findings with links, evidence, and a technology verification table.
---

# Open Source Code Research

Act as an executive research assistant. Find real code examples in open-source repositories that use the technologies, APIs, frameworks, or patterns the user needs to understand.

## Search Scope

Use the best available sources for the task:

- GitHub search, GitHub CLI, and repository code search.
- GitLab public projects and GitLab search.
- Sourcegraph, public web search, package registries, docs example repos, and vendor-maintained samples when useful.
- Local clones only when the user points to them or they are clearly relevant.

Prefer repositories with active maintenance, clear licensing, useful README docs, visible examples, tests, and production-like code.

## Workflow

1. Identify the target technologies and the kind of code example needed.
2. Build several search queries, including exact package names, API names, config keys, imports, file names, and domain-specific phrases.
3. Search GitHub first when likely to have coverage, then expand to GitLab and other public search sources.
4. Open each serious candidate's README and inspect the relevant code files.
5. Verify that the repository actually uses the claimed technologies from code, config, manifests, imports, CI files, or docs.
6. Reject examples that are toy-only, stale, unlicensed/private, unrelated, or only mention the technology without using it.
7. Return concise research findings in chat unless the user explicitly asks for a saved markdown report.

## What To Capture

For each useful repository, capture:

- Repository name, host, and link.
- License, primary language, stars/activity when visible, and last meaningful update when relevant.
- README summary: what the project claims to do, setup maturity, and whether the README is enough to learn from.
- Relevant code links with short notes about the implementation.
- Technologies verified from source evidence.
- Why the example is useful for the user's research.
- Caveats: stale dependencies, toy/demo code, missing tests, unclear license, abandoned maintenance, or incomplete docs.

## Report Format

When the user asks for a saved markdown report, use:

```markdown
# Open Source Code Research: Topic

## Summary

Short answer: best repositories to study and why.

## Recommended Repositories

| Rank | Repository | Host | Why it matters | Key code examples | Caveats |
| --- | --- | --- | --- | --- | --- |

## Technology Verification

| Repository | Technology | Evidence | Verified? | Notes |
| --- | --- | --- | --- | --- |

## README Analysis

### Repository Name

- README claim:
- What the code confirms:
- Best files to read:
- Research value:
- Caveats:
```

Use direct links for repositories and code files. Keep the summary executive-readable, but include enough evidence that the user can audit the conclusions.

## Quality Rules

- Do not rely on README claims alone; verify against code or config.
- Prefer specific file links over generic repository links.
- Distinguish "uses in production code" from "mentions in docs", "example only", or "dependency only".
- Include GitLab or another non-GitHub source when GitHub coverage is thin or the user asks to expand beyond GitHub.
- State search gaps honestly when a technology has few credible public examples.
