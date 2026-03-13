"""
Output Validator — enforces a clean document output contract.

Every mode (research paper, SRS, academic doc) must pass through this module
before content is assembled into the final formatter.  The validator:

1. Detects "meta chatter" — any assistant narration that leaked into the output.
2. Strips detectable chatter patterns via regex (fast path).
3. Reports whether the result is clean or still contains banned phrases.

Usage
-----
    from backend.agents.output_validator import sanitize_content, has_meta_chatter

    clean = sanitize_content(raw_llm_output)
    if has_meta_chatter(clean):
        # fallback: ask repair LLM or regenerate
        ...
"""
from __future__ import annotations

import re
from typing import List

# ---------------------------------------------------------------------------
# Banned phrase patterns (case-insensitive, compiled once at import time)
# ---------------------------------------------------------------------------

_BANNED_PATTERNS: List[re.Pattern] = [re.compile(p, re.IGNORECASE) for p in [
    # Opening narration phrases
    r"here is(?: the| a| your| my)?\b",
    r"here's(?: the| a| your| my)?\b",
    r"i(?:'ve| have) (written|drafted|prepared|crafted|created|generated|produced)",
    r"i(?:'ll| will) (write|draft|prepare|craft|create|generate|produce)",
    r"below(?: is| are)(?: the| a| your| my)?\b",
    r"certainly[,!]",
    r"of course[,!]",
    r"sure[,!]\s",
    r"let me\b",
    r"as requested\b",
    r"as you(?:'ve| have)? asked\b",
    r"as an ai\b",
    r"i('m| am) an ai\b",
    r"as a language model\b",
    r"please note that\b",
    r"note that\b",
    r"please (let me know|feel free)\b",
    r"let me know if\b",
    r"feel free to\b",
    r"hope(?: this)? help",
    r"i hope (this|the following)",
    r"the following is\b",
    r"polished version",
    r"here('s| is) the (polished|revised|corrected|updated|final|complete|full)",
    r"i have (written|revised|polished|corrected|completed)",
    r"the section (is|follows|below|above)\b",
    # Apologies / disclaimers
    r"i apologize\b",
    r"i('m| am) sorry\b",
    r"unfortunately\b.*\bi (cannot|can't|am unable)\b",
    # Closing chatter
    r"is there anything (else|more|further)\b",
    r"do you (want|need|have)\b.*\?",
    r"any (questions|clarifications|changes|revisions|feedback)\b.*\?",
    r"let me know\b.*\?",
]]

# Patterns for full-line removal (lines that are ONLY chatter)
_CHATTER_LINE_PATTERNS: List[re.Pattern] = [re.compile(p, re.IGNORECASE) for p in [
    r"^(here is|here's|below is|below are|the following is)\b.*$",
    r"^(certainly|of course|sure)[,!:].*$",
    r"^(please )?let me know.*$",
    r"^(hope this helps?|hope that helps?)[.!]?$",
    r"^i('ve| have) (written|drafted|prepared|crafted|created).*$",
    r"^i('ll| will) (write|draft|provide|now write).*$",
    r"^as (?:requested|asked)[,:]?.*$",
    r"^note[:]?\s+this.*$",
    r"^please note.*$",
]]

# Markdown separators used as chat-style dividers (e.g. "---" on its own line)
_MD_SEPARATOR_RE = re.compile(r"^\s*[-*_]{3,}\s*$", re.MULTILINE)


def has_meta_chatter(text: str) -> bool:
    """Return True if *text* contains any known meta-chatter phrase."""
    for pattern in _BANNED_PATTERNS:
        if pattern.search(text):
            return True
    return False


def sanitize_content(text: str) -> str:
    """
    Remove known meta-chatter from *text* and return a cleaned string.

    Strategy:
    1. Split into lines.
    2. Drop any line that matches a full-line chatter pattern.
    3. For remaining lines, remove inline chatter spans.
    4. Remove markdown horizontal rule separators (chat artefacts).
    5. Collapse multiple blank lines to at most two.
    """
    if not text:
        return text

    lines = text.splitlines()
    cleaned_lines: List[str] = []

    for line in lines:
        # Drop the entire line if it is pure chatter
        stripped = line.strip()
        drop = any(p.match(stripped) for p in _CHATTER_LINE_PATTERNS)
        if drop:
            continue

        # Remove leading chatter spans from this line (start-of-line only, to avoid
        # over-stripping legitimate content mid-sentence).
        result_line = line
        for pattern in _BANNED_PATTERNS:
            if pattern.match(result_line.lstrip()):
                result_line = pattern.sub("", result_line, count=1).lstrip(" ,:\t")

        cleaned_lines.append(result_line)

    cleaned = "\n".join(cleaned_lines)

    # Remove markdown horizontal rule separators (e.g. "---", "***", "___")
    cleaned = _MD_SEPARATOR_RE.sub("", cleaned)

    # Collapse more than two consecutive blank lines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()
