#!/bin/bash
# session_gate.sh | Injects entry-context reminder before every prompt
# related: [SHADOWMAS-LAYERING-QUICKREF, SHADOWMAS-CURRENT-TRUTH]
# phase: persistent

# --- Telemetry: one line per invocation; errors silenced ---
{
  printf '%s\t%s\t%s\t%s\n' \
    "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
    "$(basename "$0")" \
    "UserPromptSubmit" \
    "N/A" \
    >> "${CLAUDE_PROJECT_DIR:-$(pwd)}/.claude/hook-log"
} 2>/dev/null || true

echo "[GATE] Before tool use: confirm relevant entry context from 00_entry/SHADOWMAS-LAYERING-QUICKREF.v0.en.md and current truth intake from 01_truth/SHADOWMAS-CURRENT-TRUTH.v0.en.md when the task may affect repo structure, truth surfaces, packets, registry, runtime, or public/private boundaries."
exit 0
