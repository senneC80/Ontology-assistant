"""Detect and extract OntoUML envelope JSON from assistant reply text."""
from __future__ import annotations
import json
import re
from typing import Optional


def find_envelope(text: str) -> Optional[tuple[dict, int, int]]:
    """Return (envelope_dict, start, end) for the first OntoUML envelope in text.

    start and end are character indices of the full fenced block (backticks
    included), so text[:start] is prose-before and text[end:] is prose-after.
    For a bare-JSON match the span covers the entire text (0, len(text)).

    Search order:
    1. Fenced ```json blocks
    2. Fenced ``` blocks without a language tag
    3. Bare top-level JSON (fallback)

    All matches in each category are tried before moving to the next.
    Returns the first candidate that both parses as JSON and has a "model" key.
    """
    # 1. Fenced ```json blocks (no newline required immediately after "json")
    for m in re.finditer(r"```json\s*(.*?)```", text, re.DOTALL):
        try:
            obj = json.loads(m.group(1).strip())
            if isinstance(obj, dict) and "model" in obj:
                return obj, m.start(), m.end()
        except (json.JSONDecodeError, ValueError):
            continue

    # 2. Fenced ``` blocks with no language tag (negative lookahead excludes word chars)
    for m in re.finditer(r"```(?!\w)\s*(.*?)```", text, re.DOTALL):
        try:
            obj = json.loads(m.group(1).strip())
            if isinstance(obj, dict) and "model" in obj:
                return obj, m.start(), m.end()
        except (json.JSONDecodeError, ValueError):
            continue

    # 3. Bare JSON fallback: attempt to parse the full text
    try:
        obj = json.loads(text.strip())
        if isinstance(obj, dict) and "model" in obj:
            return obj, 0, len(text)
    except (json.JSONDecodeError, ValueError):
        pass

    return None


def extract_envelope(text: str) -> Optional[dict]:
    """Return the envelope dict from text, or None. Delegates to find_envelope."""
    result = find_envelope(text)
    return result[0] if result is not None else None
