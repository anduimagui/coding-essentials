---
name: local-skill-creator
description: Create or update a project-local agent skill inside the current project's `.agents/skills` folder. Use when a user asks to create, scaffold, or maintain a skill for one repository or local project only, instead of installing it in the user's machine-wide agent setup.
---

# Local Skill Creator

Create skills that belong to one project. Keep them in `<project-root>/.agents/skills/<skill-name>`.

## Workflow

1. Resolve the project root. Use the root that the user names. Otherwise, use the current Git repository root. If there is no Git repository, use the current working directory.
2. Read the project instructions, including each applicable `AGENTS.md`, before you create or change the skill.
3. Convert the requested name to lowercase hyphen-case. Make the folder name equal to the `name` field in `SKILL.md`.
4. Inspect `<project-root>/.agents/skills` and the proposed destination before you make changes.
5. For a new skill, use the standard skill creator scaffold:

   ```bash
   python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/init_skill.py" \
     <skill-name> \
     --path <project-root>/.agents/skills \
     --interface 'display_name=<Display Name>' \
     --interface 'short_description=<25-64 character description>' \
     --interface 'default_prompt=Use $<skill-name> to <example task>.'
   ```

6. Replace all scaffold placeholders. Keep `SKILL.md` compact and operational. Add `scripts`, `references`, or `assets` only when the skill needs them.
7. For an existing skill, edit it in place. Do not create a second copy or an alias.
8. Validate the completed skill:

   ```bash
   python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
     <project-root>/.agents/skills/<skill-name>
   ```

9. Test each new script that the skill contains. Report the exact local skill path and the validation result.

## Boundaries

- Do not create or install the skill in `${AGENTS_HOME:-$HOME/.agents}/skills`, `${CODEX_HOME:-$HOME/.codex}/skills`, or another machine-wide folder.
- Do not add the project-local skill to a global installer, global skills list, or machine-wide configuration.
- Do not create compatibility links in product-specific skill folders.
- Do not overwrite an existing local skill until you inspect it and confirm that the requested change applies to it.
