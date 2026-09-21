---
name: documentation-manager
description: Verify and maintain consistency between source code implementation and documentation across a codebase. Use when asked to audit docs, update docs from code, verify README/API/CLI/config examples, check generated docs, or produce a documentation verification report.
---

# Documentation Manager

Use this skill to compare what the code actually does with what the documentation claims. Prefer evidence from source files, help output, generated docs, tests, and runnable examples over assumptions.

## Discovery

1. Identify project type: CLI tool, web API, library, framework, app, or mixed project.
2. Determine the tech stack and package managers.
3. Locate source directories such as `src/`, `lib/`, `internal/`, `app/`, `cmd/`, or package-specific equivalents.
4. Locate documentation such as `README*`, `docs/`, `doc/`, wiki exports, generated references, OpenAPI specs, examples, and tutorials.
5. Identify public entry points such as CLI binaries, API routes, public package exports, config schemas, or framework hooks.

Useful commands to adapt:

```bash
find . -type f -name "README*"
find . -type f -name "*.md" | grep -E "(docs/|doc/)" || true
ls -la src/ lib/ internal/ app/ cmd/ 2>/dev/null
cat package.json pyproject.toml setup.py Cargo.toml go.mod 2>/dev/null
```

## Verification

Check the highest-value public surface first:

- Public APIs match documented signatures, return types, errors, and examples.
- CLI commands, subcommands, flags, defaults, help text, and version output match docs.
- Configuration options, environment variables, defaults, and behavior match docs.
- Installation, setup, build, and dependency instructions match the current project.
- Code examples are syntactically valid and use current APIs.
- Links and file paths still resolve.
- Generated documentation is current with source files when a generation system exists.

For automated docs, search for doc tooling and run the smallest safe generation/check command:

```bash
ls -la scripts/*doc* scripts/*gen* 2>/dev/null
rg "sphinx|jsdoc|godoc|rustdoc|doxygen|generate.*doc|build.*doc" .github .gitlab-ci.yml . 2>/dev/null
npm run docs 2>/dev/null
make docs 2>/dev/null
```

## Update Rules

- If code is current and docs are stale, update documentation.
- If docs describe intended behavior but code differs, flag the code issue instead of silently rewriting the promise.
- Highlight breaking changes that affect users.
- Remove docs for removed features when the repository clearly no longer supports them.
- Add missing docs for public features, configuration, or error behavior.
- Keep edits scoped to documentation and required generated artifacts unless implementation changes were explicitly requested.

## Report Format

Return a concise report with these sections when auditing:

```markdown
## Documentation Verification Report

### Project Information
- Project Type:
- Tech Stack:
- Documentation Location:
- Source Location:

### Working Correctly

### Minor Discrepancies

### Major Issues

### Missing Documentation

### Recommendations

### Coverage Summary
```

When making edits, also summarize which docs changed, why they now match implementation, and what verification commands ran.
