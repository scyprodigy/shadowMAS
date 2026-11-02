"""Filename convention for new packets in an external workspace.

Packet identity and contract version remain the fields inside the YAML file.
Existing workspace files are not renamed or rejected by this module.
"""

from __future__ import annotations

import re


PACKET_DIRECTORIES = {
    "task_packet": "packets",
    "memory_packet": "packets",
    "review_packet": "reviews",
}
SAFE_UID = re.compile(r"[a-z0-9](?:[a-z0-9_-]*[a-z0-9])?\Z")
VERSION = re.compile(r"v[0-9]+\Z")


def workspace_packet_name(packet_type: str, packet_uid: str, schema_version: str) -> str:
    """Return a predictable filename for a new packet, or refuse unsafe input."""
    if not isinstance(packet_type, str) or packet_type not in PACKET_DIRECTORIES:
        raise ValueError(f"unsupported packet_type: {packet_type!r}")
    if (not isinstance(packet_uid, str) or len(packet_uid) > 128
            or not SAFE_UID.fullmatch(packet_uid)):
        raise ValueError("packet_uid must be 1-128 lowercase ASCII letters, digits, '-' or '_', without punctuation at either end")
    if not isinstance(schema_version, str) or not VERSION.fullmatch(schema_version):
        raise ValueError(f"unsupported schema_version for filename: {schema_version!r}")
    return f"{packet_type}.{packet_uid}.{schema_version}.yaml"
