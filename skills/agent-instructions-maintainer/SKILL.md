---
name: agent-instructions-maintainer
description: Maintain compact repository agent instructions such as AGENTS.md, CLAUDE.md, or similar local coding-agent guidance. Use when asked to create, update, audit, shorten, or align agent instructions with the real project workflow, commands, identity rules, tests, docs, and repository conventions.
---

# Agent Instructions Maintainer

Use this skill to keep the `AGENTS.md` file in the current working directory accurate, compact, portable, and operational. Instructions should help future agents act correctly in that directory without re-discovering stable project conventions.

You are the agent updater for the current directory. Create or update `AGENTS.md` in the directory where you are running only. Never create, edit, or replace an instruction file in a parent directory, child directory, or sibling project unless the user explicitly changes the working directory and asks again.

If `AGENTS.md` already exists in the current directory, update it. If it does not exist, state that before creating a new file.

## Workflow

1. Confirm the active current directory and treat it as the only place where `AGENTS.md` may live.
2. Scan only the current directory for key files and folders: `README*`, package and config files, prompt libraries, scripts, task runners, and existing local docs.
3. Identify commands for setup, test, lint, build, install, and common workflows from files in the current directory.
4. Detect naming conventions, file layout patterns, tooling preferences, safety constraints, and project-specific rules.
5. Remove stale commands, stale paths, obsolete account assumptions, broad generic advice, and machine-specific details.
6. Write or refine `AGENTS.md` as a compact system memory file for future agents, using imperative language with short, scannable sections.
7. Exclude temporary notes, debug outputs, secrets, private tokens, private account details, and unnecessary personal-only context.
8. Preserve useful existing structure when updating, but shorten it when it is verbose.
9. Validate changed commands when practical.

## Style

- Start with an intro such as "You are..." or "Do this..." based on the depth and context of the directory.
- Prefer short imperative bullets.
- Keep the final file compact. Include only rules that prevent real future mistakes.
- Keep generic coding advice out unless it prevents a real local failure.
- Use repository-relative paths only. Do not write absolute local paths, home-directory paths, usernames, device names, or workspace locations.
- Do not include details that will not persist across machines, such as local installation paths, machine-specific ports, editor state, cache folders, generated thread IDs, or personal filesystem layout.
- Mention where commands should be run with portable labels such as "repo root" or "this directory".
- Distinguish required checks from optional checks.
- Note known blockers and escalation points clearly.

## Output

State whether `AGENTS.md` in the current directory was created or updated, then summarize what changed in 3 to 5 bullets. Include only the workflow evidence and verified commands that matter.
