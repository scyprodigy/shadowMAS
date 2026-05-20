#!/bin/bash
# check_naming.sh | Path-sensitive filename naming gate for shadowMAS surfaces
# related: [check_lang, check_header]
# phase: 1

set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')
BASENAME=$(basename "$FILE_PATH")
DIRNAME=$(dirname "$FILE_PATH")
NAME_NO_EXT="${BASENAME%.*}"

# =============================================
# Universal exemption rules
# =============================================

# Rule 1: Dotfiles and dot-directories
if echo "$BASENAME" | grep -q '^\.'; then
  exit 0
fi
if echo "$DIRNAME" | grep -Eq '(^|/)\.[^/]+'; then
  exit 0
fi

# Rule 2: All-uppercase filename (before extension)
# Matches: README.md, LICENSE, CHANGELOG.md, CONTRIBUTING.md
if echo "$NAME_NO_EXT" | grep -Pq '^[A-Z][A-Z0-9_-]*$'; then
  exit 0
fi

# Rule 3: Path under .claude/ directory
if echo "$FILE_PATH" | grep -q '/\.claude/'; then
  exit 0
fi

# Rule 4: Well-known ecosystem files
KNOWN_FILES=(
  "package.json"
  "package-lock.json"
  "tsconfig.json"
  "tsconfig.build.json"
  "pyproject.toml"
  "requirements.txt"
  "Cargo.toml"
  "Cargo.lock"
  "go.mod"
  "go.sum"
  "pnpm-lock.yaml"
  "yarn.lock"
  "Pipfile"
  "Pipfile.lock"
  "poetry.lock"
  "Makefile"
  "Dockerfile"
  "Procfile"
  "Gemfile"
  "Gemfile.lock"
  "Rakefile"
  "Vagrantfile"
  "docker-compose.yml"
  "docker-compose.yaml"
  "compose.yml"
  "compose.yaml"
  "deno.json"
  "bun.lockb"
  "__init__.py"
)

for known in "${KNOWN_FILES[@]}"; do
  if [ "$BASENAME" = "$known" ]; then
    exit 0
  fi
done

# =============================================
# Path-sensitive rules (shadowMAS path policy)
# Policy reference: 07_working/drafts/rationale/policy_filename_memo.md
# =============================================

# Rule 5: 07_working/private/ - full exemption (never tracked anyway)
if echo "$FILE_PATH" | grep -Eq '(^|/)07_working/private/'; then
  exit 0
fi

# Helper: structured_semantic pattern (UPPERCASE-WITH-HYPHENS-AND-DOTS)
match_structured_semantic() {
  echo "$1" | grep -Pq '^[A-Z][A-Z0-9-]*(\.v[0-9]+(_[0-9]+)?)?(\.[a-zA-Z][a-zA-Z0-9-]*)?$'
}

# Helper: strict 3-segment snake_case
match_strict_three_segment() {
  echo "$1" | grep -Pq '^[a-zA-Z0-9][a-zA-Z0-9-]*_[a-zA-Z0-9][a-zA-Z0-9-]*_[a-zA-Z0-9][a-zA-Z0-9-]*$'
}

# Helper: 05_scripts/-style 2-or-3-segment lowercase snake_case
match_two_or_three_segment_lowercase() {
  echo "$1" | grep -Pq '^[a-z][a-z0-9]*_[a-z][a-z0-9]*(_[a-z][a-z0-9]*)?$'
}

# Helper: examples/ fixture pattern - lowercase snake_case with 2-4 segments
match_fixture_lowercase() {
  local name="$1"
  if ! echo "$name" | grep -Pq '^[a-z][a-z0-9_]*$'; then
    return 1
  fi
  local underscore_count
  underscore_count=$(echo "$name" | awk -F_ '{print NF-1}')
  if [ "$underscore_count" -ge 1 ] && [ "$underscore_count" -le 4 ]; then
    return 0
  fi
  return 1
}

# Helper: packet-style dotted filename (e.g., task_packet.valid.v0)
match_packet_dotted() {
  echo "$1" | grep -Pq '^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_-]*)*(\.v[0-9]+(_[0-9]+)?)?$'
}

# Helper: working-marker dotted filename for 07_working/drafts/**
# Accepts files like packet_common_shell.PROPOSAL.v0, bootstrap-prompt.CLAUDE-CODE.v0,
# agents.template.PROPOSAL, shared_core.template.DRAFT, adapter-plan.v0, etc.
match_working_marker() {
  local name="$1"
  # Must be dotted-mixed shape: base segment then at least one dot-segment
  if ! echo "$name" | grep -Pq '^[a-zA-Z][a-zA-Z0-9_-]*(\.[A-Za-z0-9][A-Za-z0-9_-]*)+$'; then
    return 1
  fi
  # Must contain at least one recognised marker segment
  if ! echo ".${name}." | grep -Eq '\.(PROPOSAL|DRAFT|template|CLAUDE-CODE|v[0-9]+(_[0-9]+)?|en|zh-TW)\.'; then
    return 1
  fi
  # Base segment (before first dot) must not be a forbidden scratch token
  local base
  base=$(echo "$name" | cut -d. -f1)
  case "$base" in
    scratch|tmp|temp|notes|final)
      echo "BLOCKED: working-marker base segment is a forbidden scratch token '$base': $BASENAME" >&2
      return 1
      ;;
  esac
  return 0
}

# Helper: flexible_research check for snake_case multi-segment names
check_flexible_research() {
  local name="$1"
  local ext="$2"

  # Extension must be one of: md, yaml, yml, json, txt
  case "$ext" in
    md|yaml|yml|json|txt) ;;
    *)
      echo "BLOCKED: extension '.$ext' not allowed in flexible_research path: $BASENAME" >&2
      echo "Allowed extensions: .md, .yaml, .yml, .json, .txt" >&2
      return 1
      ;;
  esac

  # Must be lowercase snake_case
  if ! echo "$name" | grep -Pq '^[a-z][a-z0-9_]*$'; then
    echo "BLOCKED: flexible_research filename must be lowercase snake_case: $BASENAME" >&2
    return 1
  fi

  # Segment count: 2-6 segments (1-5 underscores)
  local underscore_count
  underscore_count=$(echo "$name" | awk -F_ '{print NF-1}')
  if [ "$underscore_count" -lt 1 ] || [ "$underscore_count" -gt 5 ]; then
    echo "BLOCKED: flexible_research filename must have 2 to 6 underscore segments: $BASENAME" >&2
    return 1
  fi

  # Forbidden generic scratch tokens (lowercase only; "draft" intentionally omitted -
  # the established working-adapter bundle uses uppercase .DRAFT marker which is
  # handled by the working-marker rule)
  local forbidden_tokens=("scratch" "tmp" "temp" "notes" "final")
  for token in "${forbidden_tokens[@]}"; do
    if echo "_${name}_" | grep -q "_${token}_"; then
      echo "BLOCKED: filename contains forbidden generic scratch token '$token': $BASENAME" >&2
      return 1
    fi
  done

  return 0
}

# Rule 6: 07_working/drafts/** - flexible_research with working-marker fallback
if echo "$FILE_PATH" | grep -Eq '(^|/)07_working/drafts/'; then
  if [ "$BASENAME" = "$NAME_NO_EXT" ]; then
    echo "BLOCKED: File has no extension: $BASENAME" >&2
    exit 2
  fi
  EXT="${BASENAME##*.}"
  # Accept legacy structured_semantic UPPERCASE-WITH-HYPHENS-AND-DOTS
  if match_structured_semantic "$NAME_NO_EXT"; then
    exit 0
  fi
  # Accept working-marker dotted filenames (.PROPOSAL / .DRAFT / .CLAUDE-CODE / .template / .vN)
  if match_working_marker "$NAME_NO_EXT"; then
    exit 0
  fi
  # Accept lowercase snake_case flexible_research names
  if check_flexible_research "$NAME_NO_EXT" "$EXT"; then
    exit 0
  fi
  exit 2
fi

# Rule 7: 07_working/ root - accept structured_semantic legacy or strict 3-segment or flexible_research
if echo "$FILE_PATH" | grep -Eq '(^|/)07_working/[^/]+$'; then
  if [ "$BASENAME" = "$NAME_NO_EXT" ]; then
    echo "BLOCKED: File has no extension: $BASENAME" >&2
    exit 2
  fi
  EXT="${BASENAME##*.}"
  if match_structured_semantic "$NAME_NO_EXT"; then
    exit 0
  fi
  if match_strict_three_segment "$NAME_NO_EXT"; then
    exit 0
  fi
  if check_flexible_research "$NAME_NO_EXT" "$EXT" 2>/dev/null; then
    exit 0
  fi
  echo "BLOCKED: 07_working/ root filename must be UPPERCASE-legacy, 3-segment, or flexible_research: $BASENAME" >&2
  exit 2
fi

# Rule 8: 00_entry/, 01_truth/, 03_memory/, 04_runtime/, 06_human_docs/ - structured_semantic
if echo "$FILE_PATH" | grep -Eq '(^|/)(00_entry|01_truth|03_memory|04_runtime|06_human_docs)/'; then
  if match_structured_semantic "$NAME_NO_EXT"; then
    exit 0
  fi
  if match_strict_three_segment "$NAME_NO_EXT"; then
    exit 0
  fi
  echo "BLOCKED: structured_semantic path requires UPPERCASE-WITH-HYPHENS-AND-DOTS or 3-segment snake_case name: $BASENAME" >&2
  echo "Examples: SHADOWMAS-CURRENT-TRUTH.v0.en.md, infra_auth_service.py" >&2
  exit 2
fi

# Rule 9: 02_packets/ - accept dotted-version schema or UPPERCASE explanatory doc
if echo "$FILE_PATH" | grep -Eq '(^|/)02_packets/'; then
  if echo "$NAME_NO_EXT" | grep -Pq '^[a-z][a-z0-9_]*\.v[0-9]+(_[0-9]+)?$'; then
    exit 0
  fi
  if match_structured_semantic "$NAME_NO_EXT"; then
    exit 0
  fi
  if match_strict_three_segment "$NAME_NO_EXT"; then
    exit 0
  fi
  echo "BLOCKED: 02_packets/ filename must be packet_schema.vN.ext or UPPERCASE explanatory doc or 3-segment: $BASENAME" >&2
  exit 2
fi

# Rule 10: 05_scripts/ - 2-or-3-segment lowercase, or strict 3-segment, or UPPERCASE doc
if echo "$FILE_PATH" | grep -Eq '(^|/)05_scripts/'; then
  if match_two_or_three_segment_lowercase "$NAME_NO_EXT"; then
    exit 0
  fi
  if match_strict_three_segment "$NAME_NO_EXT"; then
    exit 0
  fi
  if match_structured_semantic "$NAME_NO_EXT"; then
    exit 0
  fi
  echo "BLOCKED: 05_scripts/ filename must be 2-or-3-segment lowercase snake_case or UPPERCASE doc: $BASENAME" >&2
  exit 2
fi

# Rule 11: examples/ - fixture lowercase (2-4 segments) or packet-dotted under packets/ subpath
if echo "$FILE_PATH" | grep -Eq '(^|/)examples/'; then
  if match_fixture_lowercase "$NAME_NO_EXT"; then
    exit 0
  fi
  if echo "$FILE_PATH" | grep -Eq '(^|/)examples/packets/' && match_packet_dotted "$NAME_NO_EXT"; then
    exit 0
  fi
  if match_strict_three_segment "$NAME_NO_EXT"; then
    exit 0
  fi
  echo "BLOCKED: examples/ filename must be lowercase 2-4 segment fixture or packet-dotted under packets/: $BASENAME" >&2
  exit 2
fi

# Rule 12: tests/ - test_ prefix with any segments, or 3-segment default
if echo "$FILE_PATH" | grep -Eq '(^|/)tests/'; then
  if echo "$NAME_NO_EXT" | grep -Pq '^test_[a-z0-9][a-z0-9_]*$'; then
    exit 0
  fi
  if match_strict_three_segment "$NAME_NO_EXT"; then
    exit 0
  fi
  echo "BLOCKED: tests/ filename must be test_*.py snake_case or 3-segment: $BASENAME" >&2
  exit 2
fi

# =============================================
# Default fallback: strict 3-segment {layer}_{module}_{type}.{ext}
# Applies to tools/ and any uncovered path
# =============================================

if ! echo "$BASENAME" | grep -q '\.'; then
  echo "BLOCKED: File has no extension: $BASENAME" >&2
  echo "Expected pattern: {layer}_{module}_{type}.{ext}" >&2
  exit 2
fi

if ! match_strict_three_segment "$NAME_NO_EXT"; then
  echo "BLOCKED: Filename does not match naming convention: $BASENAME" >&2
  echo "Expected pattern: {layer}_{module}_{type}.{ext}" >&2
  echo "Example: infra_auth_service.py, core_dispatch_schema.yaml" >&2
  exit 2
fi

exit 0
