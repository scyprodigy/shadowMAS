# shadowMAS External Workspace Helper

## Purpose
This helper creates or locates an external shadowMAS workspace for a product project.

It does not write into the product project directory.

`shadowmas_packet.py` validates and writes new packets into an existing workspace.
It does not rename existing packets or edit the product project.

## Current commands
Direct commands:

```bash
python3 05_scripts/workspace/shadowmas_workspace.py init --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py where --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py inspect --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py list
python3 05_scripts/workspace/shadowmas_workspace.py destroy --project <project-path>
python3 05_scripts/workspace/shadowmas_workspace.py destroy --project <project-path> --yes
python3 05_scripts/workspace/shadowmas_packet.py write --project <project-path> --input <draft.yaml>
```

Logical future command shapes:

```bash
shadowmas workspace init --project <project-path>
shadowmas workspace where --project <project-path>
shadowmas workspace inspect --project <project-path>
shadowmas workspace list
shadowmas workspace destroy --project <project-path>
shadowmas packet write --project <project-path> --input <draft.yaml>
```

Command summary:

- `init --project <project-path>` creates the external workspace and its `workspace.json`, `packets/`, `reviews/`, `handoffs/`, and `runs/` entries under the local data root.
- `where --project <project-path>` prints the workspace path for an existing workspace.
- `inspect --project <project-path>` checks existing workspace metadata.
- `list` lists existing shadowMAS workspaces under the local data root. It is read-only, does not inspect or modify product repos, and does not create workspace artifacts.
- `destroy --project <project-path>` targets the external shadowMAS workspace for that project. Without `--yes`, it previews the workspace that would be removed. With `--yes`, it removes the external workspace. Use it carefully.
- `shadowmas_packet.py write` validates one YAML draft and places it in an existing workspace without overwriting a filename or reusing a packet UID.

## New packet filenames

For new workspace packets, the writer uses `<packet_type>.<packet_uid>.<schema_version>.yaml`.
For example, `task_packet.19c25e29-f4b5-4a17-81b2-79c85b749cbe.v0.yaml`.
`task_packet` and `memory_packet` go under `packets/`; `review_packet` goes under
`reviews/`. The writer assigns a UUID when `packet_uid` is absent. A supplied
UID must use 1–128 lowercase ASCII letters, digits, hyphens, or underscores,
and must start and end with a letter or digit. The file's fields remain the
authority for identity, type, and schema version; the filename is a mirror.

The writer refuses malformed or contract-invalid YAML, an existing UID anywhere
in the workspace's packet-bearing directories, an existing destination filename,
and a destination redirected into the product project. Its write is an explicit
operator or agent action. Existing differently named files remain readable and
are not renamed. Direct filesystem writes by other tools can bypass this
convention; agents creating new packets should call the writer.
The writer scans existing workspace YAML for UID collisions. No lookup-speed
improvement is claimed from the filename convention alone.

## Workspace boundary
Governance artifacts stay outside product repos by default. The helper writes under the external shadowMAS workspace root in the local data root, not inside the product repo.

The helper does not inspect product repo contents, run git, generate packets, call the validator, or run agents.

`inspect` is read-only. It checks whether the external workspace exists and whether `workspace.json` exists and matches the MVP metadata contract. It does not repair, migrate, write, inspect product repo contents, run git, validate packets, or run agents.

`destroy` removes only the external shadowMAS workspace when `--yes` is supplied. It does not delete the product repo.

Product-repo write-back remains manual and review-only. Do not commit workspace artifacts into a product repo unless they were intentionally reviewed and promoted by that repo's owner.

## Workspace location
Cross-platform explicit override:

```text
$SHADOWMAS_DATA_HOME/workspaces/
```

`SHADOWMAS_DATA_HOME` has precedence on every platform. It exists so tests,
portable installations, and controlled runners can select one isolated data
root without relying on host-specific variables. Use a directory dedicated to
shadowMAS; the value must be an absolute path and the helper manages its
`workspaces/` child.

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
