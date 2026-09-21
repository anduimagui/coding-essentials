#!/usr/bin/env python3
"""Validate the local skill repository layout.

Single source of truth: SKILL.md YAML frontmatter (name + description), per the
Agent Skills specification (https://agentskills.io/specification). All agents
(Pi, Claude Code, Codex, OpenCode, ChatGPT desktop) and skills.sh indexers read
only SKILL.md frontmatter, so that is the only required metadata file.

agents/openai.yaml is optional UI metadata for the OpenAI app (display name,
short description, default prompt). If present it must be well-formed and
consistent with the skill; it can be regenerated with sync-openai-yaml.py.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

SKILLS_ROOT = Path(__file__).resolve().parent
IGNORED_SKILL_DIRS = {
    ".git",
    ".github",
    ".opencode",
    "deprecated",
    "in-progress",
    "personal",
    "node_modules",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_DESCRIPTION = 1024


def skill_dirs() -> list[Path]:
    """Directories that look like skills: contain a SKILL.md."""
    return sorted(
        path
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir()
        and path.name not in IGNORED_SKILL_DIRS
        and (path / "SKILL.md").exists()
    )


def read_frontmatter(path: Path) -> dict:
    """Parse SKILL.md frontmatter as YAML. Raises ValueError on problems."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter block")
    try:
        _, raw_frontmatter, _ = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError("unterminated YAML frontmatter block") from exc
    if yaml is None:
        raise ValueError("PyYAML is required to validate skills")
    try:
        parsed = yaml.safe_load(raw_frontmatter)
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return parsed


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    name = path.name
    skill_md = path / "SKILL.md"

    if not NAME_RE.match(name):
        errors.append(f"{name}: directory name must be kebab-case")

    if not skill_md.exists():
        errors.append(f"{name}: missing SKILL.md")
        return errors

    try:
        frontmatter = read_frontmatter(skill_md)
    except (ValueError, OSError) as exc:
        errors.append(f"{name}: {exc}")
        frontmatter = {}

    if frontmatter.get("name") != name:
        errors.append(f"{name}: SKILL.md frontmatter name must match directory name")
    description = frontmatter.get("description")
    if not description or not str(description).strip():
        errors.append(f"{name}: SKILL.md frontmatter must include a description")
    elif len(str(description)) > MAX_DESCRIPTION:
        errors.append(f"{name}: SKILL.md description exceeds {MAX_DESCRIPTION} chars")

    # Optional OpenAI UI metadata. Never required; validated only when present.
    openai_yaml = path / "agents" / "openai.yaml"
    if openai_yaml.exists():
        validate_openai_yaml(openai_yaml, name, errors)

    return errors


def validate_openai_yaml(path: Path, name: str, errors: list[str]) -> None:
    if yaml is None:
        errors.append(f"{name}: agents/openai.yaml present but PyYAML is unavailable")
        return
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError) as exc:
        errors.append(f"{name}: agents/openai.yaml is not valid YAML: {exc}")
        return
    if not isinstance(data, dict) or not isinstance(data.get("interface"), dict):
        errors.append(f"{name}: agents/openai.yaml must contain an interface: mapping")
        return
    interface = data["interface"]
    for key in ("display_name", "short_description"):
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            errors.append(f"{name}: agents/openai.yaml interface.{key} must be a non-empty string")
            break
    short = interface.get("short_description")
    if isinstance(short, str) and not (25 <= len(short) <= 64):
        errors.append(
            f"{name}: agents/openai.yaml short_description must be 25-64 chars "
            f"(got {len(short)})"
        )


def main() -> int:
    skills = skill_dirs()
    if not skills:
        print("No skill directories (with SKILL.md) found.", file=sys.stderr)
        return 1

    errors = [error for skill in skills for error in validate_skill(skill)]
    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(skills)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())