---
name: git-trackability-check
description: Check current local git work and decide which changed, untracked, generated, ignored, or local-only files should be tracked versus ignored. Use when asked whether new files belong in git, whether .gitignore should change, or which local work should be staged before committing.
---

# Git Trackability Check

Use this skill to review local git work before staging. The goal is to decide what belongs in source control and what should remain ignored or local-only.

## Workflow

1. Identify the repository root with `git rev-parse --show-toplevel`.
2. Inspect local state:

```bash
git status --short --ignored
git diff --stat
git diff --name-only
git ls-files --others --exclude-standard
```

3. Read `.gitignore`, nested ignore files, package metadata, build scripts, docs, CI, and deployment config when they explain the changed paths.
4. Classify every local path that appears relevant:
   - Track source, config, docs, lockfiles, workflow files, public assets, migrations, fixtures, and intentional generated files.
   - Ignore dependencies, build output, caches, logs, editor files, OS files, local secrets, downloaded binaries, and machine-specific config.
5. Check whether ignored paths are already covered by existing patterns before recommending `.gitignore` changes.
6. Do not add broad ignore rules that would hide real source files.
7. Do not stage, commit, delete, or rewrite files unless the user explicitly asks.

## Repository Skill Folders

For skill repositories like this one, treat each skill folder as the source of record. New or updated `SKILL.md`, metadata, adapter files, scripts, references, and assets are meant to be tracked when they define installable repo-wide skills.

Prefer updating an existing skill folder when the behavior belongs to an existing workflow. Create a new skill folder only when the job has a distinct trigger, workflow, and output.

## Output

Start with a direct yes/no answer when the user asks whether current files should be tracked.

Use this shape:

```text
Yes, the new docs files are meant to be trackable.

Track these:
- `path`: why it belongs in git

Ignore these:
- `path`: why it should remain ignored or local-only

So I would not add any of those new source files to `.gitignore`. The current ignore behavior is right.
```

Mention any `.gitignore` changes only when the current ignore behavior is wrong or incomplete.
