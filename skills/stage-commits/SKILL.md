---
name: stage-commits
description: Analyze local changes using local-code-review and suggest a list of atomic commits grouped by logical work sections. Use when asked to stage commits, create commit plan, split changes into logical commits, or prepare for clean commit history.
---

# Stage Commits

This skill combines with `local-code-review` to analyze local repository changes and suggest a structured list of commits grouped by coherent sections of work. It helps create clean, atomic commit histories by grouping related changes together.

## Workflow

1. **Run local-code-review first** to understand the full scope of local changes
2. **Group changes by logical sections** (not by file order) such as:
   - API behavior changes
   - Database/schema migrations
   - UI/UX modifications
   - Test additions/modifications
   - Documentation updates
   - Tooling/configuration changes
   - Refactoring/cleanup
   - Generated assets
   - Release/version changes
3. **Suggest atomic commits** - each commit should represent one logical change
4. **Present commit plan** with commit messages following conventional commits format

## Commit Grouping Rules

- **One logical change per commit** - if a change touches multiple files for the same feature/fix, group them
- **Separate refactoring from behavior changes** - don't mix refactoring with new features
- **Tests with their implementation** - include test changes in the same commit as the code they test
- **Config/tooling separate** - configuration changes get their own commit
- **Generated files last** - or exclude if they shouldn't be committed
- **Untracked files** - suggest whether to include or add to .gitignore

## Output Format

Present a commit plan:

```text
Commit Plan (based on local-code-review analysis)

Local Work Sections Identified:
- Section 1: Description (files: a.ts, b.ts)
- Section 2: Description (files: c.ts, test/c.test.ts)
- Section 3: Description (files: config.json)

Suggested Commits:
1. feat: Description of feature
   Files: path/to/file1.ts, path/to/file2.ts
   
2. fix: Description of bug fix
   Files: path/to/bugfix.ts, test/bugfix.test.ts
   
3. refactor: Description of refactoring
   Files: path/to/refactor.ts
   
4. docs: Update documentation
   Files: README.md, docs/guide.md
   
5. chore: Update build config
   Files: package.json, tsconfig.json

Staging Commands:
git add path/to/file1.ts path/to/file2.ts
git commit -m "feat: Description of feature"

git add path/to/bugfix.ts test/bugfix.test.ts
git commit -m "fix: Description of bug fix"

# ... etc
```

## Usage

Run `local-code-review` first, then this skill will analyze the output and suggest the commit plan. Use when:
- Preparing to commit local work
- Wanting to split messy changes into clean commits
- Needing a commit plan before staging
- Reviewing work before PR creation