#!/usr/bin/env python3
"""Advisory translation drift checker.

Compares section-level embeddings between an English canonical file and a
zh-TW companion file using a local Ollama embedding model.

Output is advisory only. Embedding similarity does not arbitrate truth.
Exit code is 0 on completion (including when the embedding backend is
unavailable) and 2 only on usage / file errors. This script never blocks.

Usage:
  python3 tools/check_translation_drift.py <english_file> <zh_tw_file> [--threshold 0.6]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Tuple


DEFAULT_MODEL = "mxbai-embed-large"
DEFAULT_THRESHOLD = 0.6
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/embeddings"
HEADING_RE = re.compile(r"^#{2,3}\s+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Advisory translation drift checker (embedding-based). "
            "Output is advisory; this script never blocks."
        )
    )
    parser.add_argument("english_file", help="English canonical file (.md)")
    parser.add_argument("zh_tw_file", help="zh-TW companion file (.md)")
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"cosine similarity threshold; below = warning (default {DEFAULT_THRESHOLD})",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama embedding model (default {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--ollama-url",
        default=DEFAULT_OLLAMA_URL,
        help="Ollama embedding endpoint URL",
    )
    return parser.parse_args()


def chunk_by_heading(text: str) -> List[Tuple[str, str]]:
    """Split markdown text on `##` / `###` headings; return list of (heading, body)."""
    chunks: List[Tuple[str, str]] = []
    current_heading = "<preamble>"
    current_body: List[str] = []
    for line in text.splitlines():
        if HEADING_RE.match(line):
            if current_body:
                chunks.append((current_heading, "\n".join(current_body).strip()))
            current_heading = line.strip()
            current_body = []
        else:
            current_body.append(line)
    if current_body:
        chunks.append((current_heading, "\n".join(current_body).strip()))
    return [(h, b) for h, b in chunks if b]


def embed(text: str, model: str, url: str) -> List[float]:
    payload = json.dumps({"model": model, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["embedding"]


def cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def main() -> int:
    args = parse_args()
    en_path = Path(args.english_file)
    zh_path = Path(args.zh_tw_file)

    if not en_path.is_file():
        print(f"ERROR: english file not found: {en_path}", file=sys.stderr)
        return 2
    if not zh_path.is_file():
        print(f"ERROR: zh-TW file not found: {zh_path}", file=sys.stderr)
        return 2

    en_chunks = chunk_by_heading(en_path.read_text(encoding="utf-8"))
    zh_chunks = chunk_by_heading(zh_path.read_text(encoding="utf-8"))

    try:
        embed("ping", args.model, args.ollama_url)
    except (urllib.error.URLError, KeyError, TimeoutError, ConnectionError) as exc:
        print(
            f"ADVISORY SKIPPED: embedding backend unavailable ({exc.__class__.__name__})"
        )
        print("This check is advisory only; absence does not block work.")
        return 0

    print("ADVISORY translation drift check")
    print(f"  english:   {en_path} ({len(en_chunks)} sections)")
    print(f"  zh-TW:     {zh_path} ({len(zh_chunks)} sections)")
    print(f"  model:     {args.model}")
    print(f"  threshold: {args.threshold}")
    print("---")

    en_embeds = [(h, embed(b, args.model, args.ollama_url)) for h, b in en_chunks]
    zh_embeds = [(h, embed(b, args.model, args.ollama_url)) for h, b in zh_chunks]

    warnings = 0
    for en_h, en_e in en_embeds:
        best = max(
            ((zh_h, cosine(en_e, zh_e)) for zh_h, zh_e in zh_embeds),
            key=lambda item: item[1],
            default=(None, 0.0),
        )
        zh_h, sim = best
        flag = "OK  " if sim >= args.threshold else "WARN"
        if flag.strip() == "WARN":
            warnings += 1
        zh_label = zh_h[:60] if zh_h else "<none>"
        print(f"{flag} sim={sim:.3f}  en={en_h[:60]}  best_zh={zh_label}")

    print("---")
    print(f"summary: {warnings} warnings (advisory only)")
    print("NOTE: embedding similarity is NOT truth authority; this output is advisory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
