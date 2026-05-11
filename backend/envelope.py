"""Detect and extract OntoUML envelope JSON from assistant reply text."""
from __future__ import annotations
import json
import re
from typing import Optional


def extract_envelope(text: str) -> Optional[dict]:
    """Return the first JSON object with a 'model' key found in text.

    Search order:
    1. Fenced ```json blocks
    2. Fenced ``` blocks without a language tag
    3. Bare top-level JSON (fallback)

    All matches in each category are tried before moving to the next.
    Returns the first candidate that both parses as JSON and has a "model" key.
    """
    candidates: list[str] = []

    # 1. Fenced ```json blocks (no newline required immediately after "json")
    for m in re.finditer(r"```json\s*(.*?)```", text, re.DOTALL):
        candidates.append(m.group(1).strip())

    # 2. Fenced ``` blocks with no language tag (negative lookahead excludes word chars)
    for m in re.finditer(r"```(?!\w)\s*(.*?)```", text, re.DOTALL):
        candidates.append(m.group(1).strip())

    # 3. Bare JSON fallback: attempt to parse the full text
    candidates.append(text.strip())

    for candidate in candidates:
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict) and "model" in obj:
                return obj
        except (json.JSONDecodeError, ValueError):
            continue

    return None
