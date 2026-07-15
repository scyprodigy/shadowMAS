"""Shared read-only helpers for shadowMAS repository inspection tools.

The helpers in this module never mutate repository state. They make scans
fail closed on unreadable or malformed YAML and keep file references inside
the selected repository root.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def load_yaml_documents(
    roots: list[Path],
) -> tuple[list[tuple[Path, Any]], list[str]]:
    """Load every YAML document below roots and return documents plus errors."""

    documents: list[tuple[Path, Any]] = []
    errors: list[str] = []
    seen_paths: set[Path] = set()

    for root in roots:
        if not root.is_dir():
            errors.append(f"scan root is not a directory: {root}")
            continue
        try:
            paths = sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml"))
        except (OSError, RuntimeError) as exc:
            errors.append(f"unable to scan YAML root {root}: {exc}")
            continue
        for path in paths:
            try:
                resolved_path = path.resolve()
            except (OSError, RuntimeError) as exc:
                errors.append(f"unable to resolve YAML file {path}: {exc}")
                continue
            if resolved_path in seen_paths:
                continue
            seen_paths.add(resolved_path)
            try:
                text = path.read_text(encoding="utf-8")
                data = yaml.load(text, Loader=UniqueKeyLoader)
            except (OSError, UnicodeError) as exc:
                errors.append(f"unable to read YAML file {path}: {exc}")
                continue
            except yaml.YAMLError as exc:
                detail = " ".join(str(exc).split())
                errors.append(f"unable to parse YAML file {path}: {detail}")
                continue
            documents.append((path, data))

    return documents, errors


def resolve_repo_reference(repo: Path, value: object) -> tuple[Path | None, str | None]:
    """Resolve a non-empty repository-relative path without allowing escape."""

    if not isinstance(value, str) or not value.strip():
        return None, "path must be a non-empty string"

    raw = Path(value)
    if raw.is_absolute():
        return None, "absolute paths are not repository-relative"
    if ".." in raw.parts:
        return None, "parent traversal is not allowed in repository references"

    repo_root = repo.resolve()
    try:
        target = (repo_root / raw).resolve()
        target.relative_to(repo_root)
    except (OSError, RuntimeError, ValueError):
        return None, "path resolves outside the repository root"
    return target, None
