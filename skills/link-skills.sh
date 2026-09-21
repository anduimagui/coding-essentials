#!/usr/bin/env bash
set -euo pipefail

# Links every stable skill in the repository to ~/.claude/skills, matching the
# local Claude CLI workflow used by mattpocock/skills.

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
DEST="$HOME/.claude/skills"

if [ -L "$DEST" ]; then
  resolved="$(python3 -c 'import pathlib, sys; print(pathlib.Path(sys.argv[1]).resolve())' "$DEST")"
  case "$resolved" in
    "$SKILLS_DIR"|"$SKILLS_DIR"/*)
      echo "error: $DEST is a symlink into this repo ($resolved)." >&2
      echo "Remove it and re-run; the script will recreate it as a real directory." >&2
      exit 1
      ;;
  esac
fi

mkdir -p "$DEST"

find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -name SKILL.md \
  -not -path '*/node_modules/*' \
  -not -path '*/deprecated/*' \
  -not -path '*/in-progress/*' \
  -not -path '*/personal/*' \
  -print0 |
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  name="$(basename "$src")"
  target="$DEST/$name"

  if [ -e "$target" ] && [ ! -L "$target" ]; then
    rm -rf "$target"
  fi

  ln -sfn "$src" "$target"
  echo "linked $name -> $src"
done
