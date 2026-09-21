#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"

cd "$REPO_ROOT"
find . -mindepth 2 -maxdepth 2 -name SKILL.md \
  -not -path './deprecated/*' \
  -not -path './in-progress/*' \
  -not -path './personal/*' \
  -not -path '*/node_modules/*' |
  sort
