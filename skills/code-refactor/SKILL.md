---
name: code-refactor
description: Refactor recently edited code into cleaner, better-scoped files, components, helpers, or asset folders. Use when asked to clean up a working implementation, move code out of test or work-in-progress files, reduce git conflicts, recontextualize comments, or simplify nested component props such as keeping pass-through defaults inside rest props.
---

# Code Refactor

Use this skill to turn working code into maintainable code. Treat the current edits as evidence: inspect what changed, infer what purpose the code now serves, and move it to the smallest durable home that fits the codebase.

## Workflow

1. Inspect the changed files and nearby existing patterns before editing. Use `git diff`, `rg`, adjacent files, route/component structure, tests, and asset folders to understand where similar code already lives.
2. Identify whether the edited code still belongs in its enclosing file. Split it out when it now has a clearer purpose than the parent file, is reused or likely to be reused, creates merge-conflict pressure, or is only present because it began as a test, spike, prototype, or work-in-progress build.
3. Prefer existing homes over new ones. Move code into established sibling modules, feature folders, shared utilities, route-level components, test helpers, fixture folders, prompt folders, static-data folders, or asset-type folders when those already exist and match the ownership boundary.
4. Create a new file only when no existing file is a good fit and the extracted unit has a stable name, purpose, and import path.
5. Keep the public surface small. Export only what callers need, avoid broad index files unless the repo uses them, and preserve existing import style.
6. Re-run the relevant formatter, typecheck, tests, or focused app verification after moving code.

## Refactor Checks

- File purpose: Does each file now have one understandable job?
- Ownership: Is code under the feature, route, package, or shared area that would own future changes?
- Conflict reduction: Did large edited blocks move out of crowded files when doing so makes future parallel edits easier?
- Naming: Do filenames and exported symbols describe the wider purpose, not the temporary context where the code first appeared?
- Dependency direction: Did extraction avoid importing feature-specific code into generic/shared modules?
- Tests and fixtures: Did test-only code move into test helpers or fixture/data folders instead of production modules?
- Assets: Did images, styles, JSON, prompts, templates, or static data move to the repo's existing asset/data conventions when applicable?

## Comments

Treat comments as part of the refactor. Update or remove comments that describe old prototype context, old parent-file assumptions, or now-obvious mechanics.

Keep comments only when they explain non-obvious intent, constraints, browser/API quirks, data provenance, or a decision that future maintainers would otherwise rediscover.

## Nested Props

When refactoring nested components, do not destructure props just to pass them onward.

Prefer this:

```tsx
function Parent({ title, ...childProps }: ParentProps) {
  return <Child {...childProps} title={title} />;
}
```

Avoid this when `Parent` does not use the defaults directly:

```tsx
function Parent({ title, variant = "compact", disabled = false }: ParentProps) {
  return <Child title={title} variant={variant} disabled={disabled} />;
}
```

Keep defaults close to the component that actually consumes them, unless the parent intentionally owns that behavior.

## Reporting

In the final response, summarize what moved, why it belongs there now, and what verification ran. Mention any intentionally deferred extraction when the blast radius was not worth it.
