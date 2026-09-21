#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: instructions/set-global-agents.sh [--dry-run] [--force]

Symlink instructions/AGENTS.md into global agent config locations:
  ~/.pi/agent/AGENTS.md
  ~/.claude/CLAUDE.md
  ~/.codex/AGENTS.md
  ~/.gemini/GEMINI.md
  ~/.config/opencode/AGENTS.md

Options:
  --dry-run  Print the changes without applying them.
  --force    Replace existing files or symlinks at the target paths.
  -h, --help Show this help text.
EOF
}

dry_run=0
force=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)
      dry_run=1
      ;;
    --force)
      force=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

script_dir="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_file="${script_dir}/AGENTS.md"

if [ ! -f "${source_file}" ]; then
  echo "Source file not found: ${source_file}" >&2
  exit 1
fi

targets=(
  "${HOME}/.pi/agent/AGENTS.md"
  "${HOME}/.claude/CLAUDE.md"
  "${HOME}/.codex/AGENTS.md"
  "${HOME}/.gemini/GEMINI.md"
  "${HOME}/.config/opencode/AGENTS.md"
)

run() {
  if [ "${dry_run}" -eq 1 ]; then
    printf 'dry-run:'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

link_target() {
  local target="$1"
  local target_dir
  target_dir="$(dirname "${target}")"

  run mkdir -p "${target_dir}"

  if [ -L "${target}" ]; then
    local current
    current="$(readlink "${target}")"
    if [ "${current}" = "${source_file}" ]; then
      echo "Already linked: ${target} -> ${source_file}"
      return
    fi

    if [ "${force}" -ne 1 ]; then
      echo "Refusing to replace symlink without --force: ${target} -> ${current}" >&2
      return 1
    fi
  elif [ -e "${target}" ]; then
    if [ "${force}" -ne 1 ]; then
      echo "Refusing to replace existing file without --force: ${target}" >&2
      return 1
    fi
  fi

  run ln -sfn "${source_file}" "${target}"
  if [ "${dry_run}" -eq 1 ]; then
    echo "Would link: ${target} -> ${source_file}"
  else
    echo "Linked: ${target} -> ${source_file}"
  fi
}

for target in "${targets[@]}"; do
  link_target "${target}"
done
