#!/bin/bash
# check_header.sh | Validates 3-line header on .md/.yaml/.yml files
# related: [check_lang, check_naming]
# phase: 1

set -euo pipefail

INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name')
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')
BASENAME=$(basename "$FILE_PATH")
EXT="${BASENAME##*.}"

# --- Gate: only check .md, .yaml, .yml ---
case "$EXT" in
  md|yaml|yml) ;;
  *) exit 0 ;;
esac

# --- Exempt: CLAUDE.md at any depth ---
if [ "$BASENAME" = "CLAUDE.md" ]; then
  exit 0
fi

# --- Exempt: machine-first canonical YAML surfaces (pure-data, no header convention) ---
# These files predate the 3-line header rule and carry schema/registry payload on line 1.
# The hook should not flag absent headers on them.
case "$EXT" in
  yaml|yml)
    if echo "$FILE_PATH" | grep -Eq '(^|/)02_packets/[^/]+\.(yaml|yml)$'; then
      exit 0
    fi
    if echo "$FILE_PATH" | grep -Eq '(^|/)03_memory/registry/[^/]+\.(yaml|yml)$'; then
      exit 0
    fi
    if echo "$FILE_PATH" | grep -Eq '(^|/)07_working/drafts/rationale/[^/]+\.(yaml|yml)$'; then
      exit 0
    fi
    if echo "$FILE_PATH" | grep -Eq '(^|/)examples/packets/[^/]+\.(yaml|yml)$'; then
      exit 0
    fi
    if echo "$FILE_PATH" | grep -Eq '(^|/)07_working/drafts/packet/[^/]+\.(yaml|yml)$'; then
      exit 0
    fi
    if echo "$FILE_PATH" | grep -Eq '(^|/)07_working/drafts/runtime_adapter/.*\.(yaml|yml)$'; then
      exit 0
    fi
    if echo "$FILE_PATH" | grep -Eq '(^|/)07_working/drafts/[^/]+\.(yaml|yml)$'; then
      exit 0
    fi
    ;;
esac

# --- Exempt: shadowMAS root README.md GitHub-facing landing page ---
# This is intentionally project-specific; nested README.md files still require the 3-line header.
# Resolve the project root portably: prefer CLAUDE_PROJECT_DIR, otherwise fall back to git toplevel.
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$FILE_PATH")" rev-parse --show-toplevel 2>/dev/null)}"
if [ -n "$PROJECT_ROOT" ] && [ "$FILE_PATH" = "$PROJECT_ROOT/README.md" ]; then
  exit 0
fi

# --- Get file content ---
if [ "$EVENT" = "PreToolUse" ]; then
  # Edit PreToolUse: skip — header check done on PostToolUse after file is written
  if [ "$TOOL" = "Edit" ]; then
    exit 0
  fi
  CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content')
elif [ "$EVENT" = "PostToolUse" ]; then
  if [ ! -f "$FILE_PATH" ]; then
    exit 0
  fi
  CONTENT=$(cat "$FILE_PATH")
else
  exit 0
fi

# --- Validate header (accept hybrid 3-line metadata OR legacy filename-H1) ---
LINE1=$(echo "$CONTENT" | sed -n '1p')
LINE2=$(echo "$CONTENT" | sed -n '2p')
LINE3=$(echo "$CONTENT" | sed -n '3p')

# Legacy canonical filename-H1 form: e.g. "# SHADOWMAS-OPERATOR-GUIDE.v0.en.md"
# Requires uppercase/digit name with at least one hyphen segment and at least one dot suffix.
if echo "$LINE1" | grep -Pq '^# [A-Z][A-Z0-9]*(-[A-Z0-9]+)+(\.[a-zA-Z0-9-]+)+$'; then
  exit 0
fi

ERRORS=""

if ! echo "$LINE1" | grep -Pq '^# .+ \| .+'; then
  ERRORS="${ERRORS}\n  Line 1 must match: # {name} | {responsibility}"
  ERRORS="${ERRORS}\n  Got: $LINE1"
fi
if ! echo "$LINE2" | grep -Pq '^# related: \[.*\]'; then
  ERRORS="${ERRORS}\n  Line 2 must match: # related: [{modules}]"
  ERRORS="${ERRORS}\n  Got: $LINE2"
fi
if ! echo "$LINE3" | grep -Pq '^# phase: .+'; then
  ERRORS="${ERRORS}\n  Line 3 must match: # phase: {value}"
  ERRORS="${ERRORS}\n  Got: $LINE3"
fi

if [ -n "$ERRORS" ]; then
  MSG="Header validation failed: $FILE_PATH$ERRORS"
  if [ "$EVENT" = "PreToolUse" ]; then
    echo -e "BLOCKED: $MSG" >&2
    exit 2
  elif [ "$EVENT" = "PostToolUse" ]; then
    jq -n --arg reason "$(echo -e "$MSG")" \
      '{"decision": "block", "reason": $reason}'
    exit 0
  fi
fi

exit 0
