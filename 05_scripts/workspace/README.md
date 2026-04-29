# shadowMAS External Workspace Helper

## Purpose
This helper creates or locates an external shadowMAS workspace for a product project.

It does not write into the product project directory.

## Current commands
Direct commands:

```bash
python3 05_scripts/workspace/shadowmas_workspace.py init --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py where --project <project-path>
```

Logical future command shapes:

```bash
shadowmas workspace init --project <project-path>
shadowmas workspace where --project <project-path>
```

## Workspace boundary
Governance artifacts stay outside product repos by default.

The helper does not inspect product repo contents, run git, generate packets, call the validator, or run agents.

## Workspace location
Linux / WSL:

```text
$XDG_DATA_HOME/shadowmas/workspaces/
```

Fallback:

```text
~/.local/share/shadowmas/workspaces/
```

macOS:

```text
~/Library/Application Support/shadowmas/workspaces/
```

Windows:

```text
%LOCALAPPDATA%\shadowmas\workspaces\
```

Fallback:

```text
~/AppData/Local/shadowmas/workspaces/
```

## Workspace structure
`init` creates:

```text
<workspace>/
  workspace.json
  packets/
  reviews/
  handoffs/
  runs/
```

## What it does not do
It does not:

- write into the product project directory
- inspect product repo contents
- run git
- generate packets
- call the validator
- run agents

## Exit codes
- `0`: success
- `1`: expected user-facing error, such as missing project path, non-directory project path, or missing workspace for `where`
- `2`: usage or unexpected failure

## Development notes
- Use `python3`.
- Use source-level compile checks to avoid `__pycache__` pollution:

```bash
python3 - <<'PY'
from pathlib import Path

path = "05_scripts/workspace/shadowmas_workspace.py"
source = Path(path).read_text(encoding="utf-8")
compile(source, path, "exec")
print("syntax ok")
PY
```
