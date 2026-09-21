#!/usr/bin/env bash
set -euo pipefail

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$repo_root"

target="all"
if [[ $# -gt 0 && "$1" != --* ]]; then
  target="$1"
  shift
fi

case "$target" in
  all|codex|claude|opencode) ;;
  *)
    printf 'Unknown install target: %s\n' "$target" >&2
    printf 'Usage: ./install.sh [all|codex|claude|opencode] [--skill NAME] [--dry-run] [--no-validate] [--dest PATH]\n' >&2
    exit 2
    ;;
esac

INSTALL_TARGET="$target" REPO_ROOT="$repo_root" python3 - "$@" <<'PY'
from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import sys
from pathlib import Path


IGNORED_COPY_NAMES = {".DS_Store", "__pycache__"}
TARGET_ORDER = ["codex", "claude", "opencode"]
TARGET_LABELS = {
    "codex": "Codex",
    "claude": "Claude Code",
    "opencode": "OpenCode",
}
RESTART_MESSAGES = {
    "codex": "Restart Codex to pick up installed skills.",
    "claude": "Restart Claude Code to pick up installed skills.",
    "opencode": "Restart OpenCode to pick up installed skills.",
}
REPO_ROOT = Path(os.environ["REPO_ROOT"])


def default_destination(target: str) -> Path:
    if target == "codex":
        return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills"
    if target == "claude":
        return Path.home() / ".claude" / "skills"
    if target == "opencode":
        return Path(
            os.environ.get("OPENCODE_CONFIG_DIR", Path.home() / ".config" / "opencode")
        ) / "skills"
    raise ValueError(f"Unknown install target: {target}")


def load_validator():
    validator_path = REPO_ROOT / "validate-skills.py"
    spec = importlib.util.spec_from_file_location("validate_skills", validator_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load validator from {validator_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate_skills = load_validator()


def skill_dirs(selected: list[str] | None = None) -> list[Path]:
    skills = validate_skills.skill_dirs()
    if not selected:
        return skills

    by_name = {path.name: path for path in skills}
    missing = sorted(set(selected) - set(by_name))
    if missing:
        raise ValueError(f"Unknown skill name(s): {', '.join(missing)}")
    return [by_name[name] for name in selected]


def ignore_names(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in IGNORED_COPY_NAMES or name.endswith(".pyc")}


def validate_selected(skills: list[Path]) -> None:
    errors = [error for skill in skills for error in validate_skills.validate_skill(skill)]
    if errors:
        print("Skill validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)


def replace_skill(source: Path, destination_root: Path, dry_run: bool) -> None:
    destination = destination_root / source.name
    temp_destination = destination_root / f".{source.name}.tmp-{os.getpid()}"
    backup_destination = destination_root / f".{source.name}.backup-{os.getpid()}"

    if dry_run:
        action = "update" if destination.exists() else "install"
        print(f"Would {action} {source.name} -> {destination}")
        return

    shutil.rmtree(temp_destination, ignore_errors=True)
    shutil.rmtree(backup_destination, ignore_errors=True)

    shutil.copytree(source, temp_destination, ignore=ignore_names)
    try:
        if destination.exists():
            destination.rename(backup_destination)
        temp_destination.rename(destination)
    except Exception:
        shutil.rmtree(destination, ignore_errors=True)
        if backup_destination.exists():
            backup_destination.rename(destination)
        raise
    else:
        shutil.rmtree(backup_destination, ignore_errors=True)

    print(f"Installed {source.name} -> {destination}")


def parse_args(argv: list[str], target: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=f"./install.sh {target}" if target != "all" else "./install.sh",
        description="Install skills from this repository into Codex, Claude Code, and/or OpenCode.",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="Skill destination root. Only valid when installing a single target.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        help="Install only this skill name. Can be passed more than once.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be installed without changing files.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip metadata validation before installing.",
    )
    args = parser.parse_args(argv)
    if target == "all" and args.dest is not None:
        parser.error("--dest can only be used with one target: codex, claude, or opencode")
    return args


def install_target(target: str, skills: list[Path], args: argparse.Namespace) -> None:
    destination_root = (args.dest if args.dest is not None else default_destination(target)).expanduser()
    if not args.dry_run:
        destination_root.mkdir(parents=True, exist_ok=True)

    print(f"\n{TARGET_LABELS[target]} -> {destination_root}")
    for skill in skills:
        replace_skill(skill, destination_root, args.dry_run)

    verb = "Would install" if args.dry_run else "Installed"
    print(f"{verb} {len(skills)} skill(s) into {destination_root}")
    print(RESTART_MESSAGES[target])


def main(argv: list[str]) -> int:
    target = os.environ["INSTALL_TARGET"]
    args = parse_args(argv, target)
    targets = TARGET_ORDER if target == "all" else [target]

    try:
        skills = skill_dirs(args.skill)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    if not skills:
        print("No skill directories found.", file=sys.stderr)
        return 1

    if not args.no_validate:
        validate_selected(skills)

    for install_target_name in targets:
        install_target(install_target_name, skills, args)

    return 0


raise SystemExit(main(sys.argv[1:]))
PY
