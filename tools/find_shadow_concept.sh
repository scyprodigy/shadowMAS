#!/bin/bash
# find_shadow_concept | grep one pattern across shadowMAS truth, packet, memory, runtime, human-doc, and working-draft surfaces
# related: [check_no_pollution, check_translation_drift]
# phase: tool
#
# Usage:
#   tools/find_shadow_concept.sh <pattern> [path ...]
#
# Default search surfaces (override by passing explicit paths after pattern):
#   01_truth/  02_packets/  03_memory/  04_runtime/  06_human_docs/  07_working/drafts/
#
# Pattern is an extended regex (grep -E). Filenames included: md, yaml, yml, json, py, sh.
# Filenames excluded: __pycache__/, .git/, *.pyc.

set -euo pipefail

DEFAULT_PATHS=(
  "01_truth"
  "02_packets"
  "03_memory"
  "04_runtime"
  "06_human_docs"
  "07_working/drafts"
)

if [ "$#" -eq 0 ]; then
  echo "usage: $(basename "$0") <pattern> [path ...]" >&2
  echo "       searches default truth/packet/memory/runtime/doc/draft surfaces" >&2
  exit 2
fi

pattern="$1"
shift

if [ "$#" -eq 0 ]; then
  paths=("${DEFAULT_PATHS[@]}")
else
  paths=("$@")
fi

# Filter out missing paths to avoid grep noise; keep ordering.
existing=()
for p in "${paths[@]}"; do
  if [ -e "$p" ]; then
    existing+=("$p")
  fi
done

if [ "${#existing[@]}" -eq 0 ]; then
  echo "no valid search paths under current working directory" >&2
  exit 2
fi

grep -rniIE \
  --exclude-dir='__pycache__' \
  --exclude-dir='.git' \
  --include='*.md' \
  --include='*.yaml' \
  --include='*.yml' \
  --include='*.json' \
  --include='*.py' \
  --include='*.sh' \
  "$pattern" "${existing[@]}"
