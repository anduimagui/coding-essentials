---
name: file-locator
description: Locate the files in a specified codebase that contain or support code related to one or more user queries. Use when the user asks where a feature, behavior, API, component, configuration, data flow, error, symbol, or implementation lives and wants a concise list of relevant files rather than a full code explanation or a code change.
---

# File Locator

Search one codebase and return the smallest useful set of files for each query.

## Workflow

1. Confirm the codebase root from the request or current workspace. Do not search outside it.
2. Convert each query into search terms. Include exact text, likely symbols, imports, route names, configuration keys, filenames, and domain terms.
3. List the repository files with `rg --files`. Read repository instruction files that apply to the search scope.
4. Search with `rg` first. Use several narrow searches when one broad search produces noise.
5. Inspect each promising match. Follow imports, exports, callers, registrations, routes, tests, schemas, and configuration only as needed to confirm relevance.
6. Separate primary implementation files from supporting files. Exclude generated files, vendored code, build output, lockfiles, and unrelated text matches unless the query specifically requires them.
7. Stop when the result identifies the implementation path well enough for the user to continue.

For conceptual queries, search by behavior and structure, not only by the user's exact words. For example, a query about “login redirects” can require searches for route guards, session checks, middleware, and redirect calls.

## Output

Return results in chat. Group them by query when the user gives more than one query.

Use this format:

```markdown
## Query: <query>

- `path/to/file.ts:42` — Primary implementation. Short reason this file matches.
- `path/to/file.test.ts:18` — Supporting test. Short reason this file matches.
```

Use repository-relative paths and add a line number for the strongest location when available. Order primary implementation files first, then entry points, configuration, types, and tests. Do not include a file unless its contents were inspected and its relevance was confirmed.

If no match is confirmed, state that clearly and list the terms and areas searched. Distinguish no match from an incomplete search caused by missing files, unavailable dependencies, or an invalid codebase path.

## Boundaries

- Do not edit code unless the user separately asks for a change.
- Do not return every text match. Return the files that help answer the query.
- Do not claim that a file contains an implementation when it only mentions, imports, or tests it.
- Keep explanations short. This skill produces a file map, not a full architecture report.
