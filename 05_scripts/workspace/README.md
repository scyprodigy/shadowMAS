# shadowMAS External Workspace Helper

## Purpose
This helper creates or locates an external shadowMAS workspace for a product project.

It does not write into the product project directory.

## Current commands
Direct commands:

```bash
python3 05_scripts/workspace/shadowmas_workspace.py init --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py where --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py inspect --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py list
python3 05_scripts/workspace/shadowmas_workspace.py destroy --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py destroy --project <project-path> --yes
```

Logical future command shapes:

```bash
shadowmas workspace init --project <project-path>
shadowmas workspace where --project <project-path>
shadowmas workspace inspect --project <project-path>
shadowmas workspace list
shadowmas workspace destroy --project <project-path>
```

Command summary:

- `init --project <project-path>` creates the external workspace and its `workspace.json`, `packets/`, `reviews/`, `handoffs/`, and `runs/` entries under the local data root.
- `where --project <project-path>` prints the workspace path for an existing workspace.
- `inspect --project <project-path>` checks existing workspace metadata.
- `list` lists existing shadowMAS workspaces under the local data root. It is read-only, does not inspect or modify product repos, and does not create workspace artifacts.
- `destroy --project <project-path>` targets the external shadowMAS workspace for that project. Without `--yes`, it previews the workspace that would be removed. With `--yes`, it removes the external workspace. Use it carefully.

## Workspace boundary
Governance artifacts stay outside product repos by default. The helper writes under the external shadowMAS workspace root in the local data root, not inside the product repo.

The helper does not inspect product repo contents, run git, generate packets, call the validator, or run agents.

`inspect` is read-only. It checks whether the external workspace exists and whether `workspace.json` exists and matches the MVP metadata contract. It does not repair, migrate, write, inspect product repo contents, run git, validate packets, or run agents.

`destroy` removes only the external shadowMAS workspace when `--yes` is supplied. It does not delete the product repo.

Product-repo write-back remains manual and review-only. Do not commit workspace artifacts into a product repo unless they were intentionally reviewed and promoted by that repo's owner.

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
- delete the product project directory
- promote or write back product-repo changes
- repair workspaces
- migrate workspace metadata
- inspect product repo contents
- run git
- generate packets
- call the validator
- validate packets
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
