---
name: change-summary
description: Summarize per-file changes from the current session or a given diff, focusing on file paths and function signatures rather than implementation bodies. Use when asked to recap what just changed, summarize work done in each file, review a big change without reading the full diff, or surface anything weird from recent edits.
---

# Change Summary

Use this skill to produce a tight per-file recap of recent work so the reviewer can scan it instead of reading the full diff. The goal is fast signal: which files changed, what function signatures moved, and one line on why. Skip function bodies.

## Workflow

1. Determine the change scope from the request:
   - Current session: uncommitted staged + unstaged + untracked work.
   - Recent commits: a commit range or `HEAD` against a base branch.
   - A supplied diff, patch, or PR.
2. List the changed files with their change type (added / modified / deleted / renamed).
3. For each modified or added file, extract the public surface that changed: new, changed, or removed function, method, class, type, and exported signatures. Include names, parameters, return types, and exported symbols. Do not paste bodies.
4. Add a one-line purpose per file explaining why it was touched.
5. Flag anything weird: unexpected files, surprise deletions, renamed public APIs, new dependencies, generated files, or scope creep outside the request.

## What to Include

- File path and change type.
- Function, method, class, type, and export signatures that were added, changed, or removed.
- One-line purpose per file.
- A short "Weird / unexpected" callout section when anything stands out.

## What to Skip

- Function bodies and implementation logic.
- Full pasted diffs or large code blocks.
- Unchanged files and cosmetic-only noise unless it hides a real change.

## Output

Return one block per file, ordered by how much it matters, using this shape:

```text
path/to/file.ts — modified
  + function foo(bar: string): Promise<Result>
  ~ function baz(): void  ->  baz(opts?: Opts): void
  - function oldHelper(): void
  why: add async foo, widen baz opts, drop unused oldHelper
```

Close with a short "Weird / unexpected" section listing anything that does not match the stated intent, or say "Nothing unexpected" if the change is clean.
