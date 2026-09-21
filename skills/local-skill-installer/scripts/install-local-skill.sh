#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s [--link] [--force] [--dry-run] SOURCE_SKILL_DIR\n' "${0##*/}" >&2
}

mode=copy
force=false
dry_run=false

while (($#)); do
  case "$1" in
    --link) mode=link ;;
    --force) force=true ;;
    --dry-run) dry_run=true ;;
    -h|--help) usage; exit 0 ;;
    --*) printf 'Unknown option: %s\n' "$1" >&2; usage; exit 2 ;;
    *)
      if [[ -n "${source_dir:-}" ]]; then
        printf 'Only one source skill directory may be supplied.\n' >&2
        usage
        exit 2
      fi
      source_dir=$1
      ;;
  esac
  shift
done

if [[ -z "${source_dir:-}" ]]; then
  usage
  exit 2
fi

if [[ ! -d "$source_dir" || ! -f "$source_dir/SKILL.md" ]]; then
  printf 'Source must be a directory containing SKILL.md: %s\n' "$source_dir" >&2
  exit 1
fi

source_dir=$(cd "$source_dir" && pwd -P)
skill_name=$(awk '
  NR == 1 && $0 == "---" { in_frontmatter=1; next }
  in_frontmatter && $0 == "---" { exit }
  in_frontmatter && /^name:[[:space:]]*/ {
    sub(/^name:[[:space:]]*/, "")
    gsub(/"/, "")
    print
    exit
  }
' "$source_dir/SKILL.md")

if [[ ! "$skill_name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  printf 'Invalid or missing skill name in SKILL.md: %s\n' "${skill_name:-<missing>}" >&2
  exit 1
fi

if [[ "${source_dir##*/}" != "$skill_name" ]]; then
  printf 'Source folder name (%s) must match skill name (%s).\n' "${source_dir##*/}" "$skill_name" >&2
  exit 1
fi

skills_root="${AGENTS_HOME:-$HOME/.agents}/skills"
destination="$skills_root/$skill_name"

printf '%s %s -> %s\n' "$mode" "$source_dir" "$destination"
if $dry_run; then
  exit 0
fi

mkdir -p "$skills_root"
if [[ -e "$destination" || -L "$destination" ]]; then
  if ! $force; then
    printf 'Destination already exists; inspect it or rerun with --force: %s\n' "$destination" >&2
    exit 1
  fi
  rm -rf "$destination"
fi

if [[ "$mode" == link ]]; then
  ln -s "$source_dir" "$destination"
else
  cp -R "$source_dir" "$destination"
fi

test -f "$destination/SKILL.md"
printf 'Installed %s at %s\n' "$skill_name" "$destination"
