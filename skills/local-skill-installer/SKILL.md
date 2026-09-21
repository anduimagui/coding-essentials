---
name: local-skill-installer
description: Install a skill from a local working directory into the current user's machine-wide `${AGENTS_HOME:-$HOME/.agents}/skills` folder so all compatible agent tools can discover it. Use when a user asks to install, register, link, or make a locally developed skill globally available.
---

# Local Skill Installer

Install local skills into `${AGENTS_HOME:-$HOME/.agents}/skills`. Treat that as the canonical global skill directory for the current user.

## Workflow

1. Resolve the source skill folder to an absolute path.
2. Confirm it contains `SKILL.md` and that its folder name matches the frontmatter `name`.
3. Inspect the source and destination before changing anything.
4. Run the bundled installer:

   ```bash
   scripts/install-local-skill.sh /absolute/path/to/skill
   ```

5. Verify the installed `SKILL.md` exists and report its exact path.

## Installation modes

- Use the default copy mode for a stable, independent global installation.
- Use `--link` for a skill under active development so global discovery tracks the working folder.
- Use `--dry-run` to preview the source and destination.
- Use `--force` only after inspecting an existing destination and confirming replacement is intended.

```bash
scripts/install-local-skill.sh --link /absolute/path/to/skill
scripts/install-local-skill.sh --dry-run /absolute/path/to/skill
scripts/install-local-skill.sh --force /absolute/path/to/skill
```

Do not install into product-specific folders such as `~/.codex/skills` or `~/.claude/skills` unless the user explicitly requests a compatibility link.
