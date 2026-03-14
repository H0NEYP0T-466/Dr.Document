"""Unit tests for backend.agents.output_validator

Run with:
    cd /path/to/Dr.Document
    python -m pytest backend/test_output_validator.py -v
"""
import sys
import os

# Allow running from repo root without installing the package
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from backend.agents.output_validator import has_meta_chatter, sanitize_content


# ---------------------------------------------------------------------------
# has_meta_chatter
# ---------------------------------------------------------------------------

class TestHasMetaChatter:
    def test_clean_content_passes(self):
        clean = (
            "The system implements a multi-agent pipeline for documentation generation. "
            "Repository files are cloned, summarised, and passed to specialised agents."
        )
        assert not has_meta_chatter(clean)

    def test_here_is_detected(self):
        assert has_meta_chatter("Here is the Introduction section for your paper.")

    def test_heres_detected(self):
        assert has_meta_chatter("Here's a polished version of your abstract:")

    def test_below_is_detected(self):
        assert has_meta_chatter("Below is the completed Implementation section.")

    def test_certainly_detected(self):
        assert has_meta_chatter("Certainly! I have written the following section.")

    def test_let_me_know_detected(self):
        assert has_meta_chatter("Let me know if you need any changes to this section.")

    def test_hope_this_helps_detected(self):
        assert has_meta_chatter("I hope this helps! Feel free to ask for revisions.")

    def test_as_an_ai_detected(self):
        assert has_meta_chatter("As an AI, I cannot access external resources directly.")

    def test_polished_version_detected(self):
        assert has_meta_chatter("Here is the polished version of your Introduction:")

    def test_i_have_written_detected(self):
        assert has_meta_chatter("I have written the Implementation section as requested.")

    def test_let_me_detected(self):
        assert has_meta_chatter("Let me craft the abstract for this repository.")

    def test_i_will_write_detected(self):
        assert has_meta_chatter("I'll write a concise abstract for you now.")

    def test_case_insensitive(self):
        assert has_meta_chatter("HERE IS THE INTRODUCTION:")
        assert has_meta_chatter("here is the introduction:")


# ---------------------------------------------------------------------------
# sanitize_content
# ---------------------------------------------------------------------------

class TestSanitizeContent:
    def test_clean_content_unchanged(self):
        clean = (
            "The repository implements a FastAPI backend with a React frontend. "
            "The codebase consists of multiple agents, each responsible for a distinct "
            "documentation generation task."
        )
        result = sanitize_content(clean)
        assert result == clean

    def test_removes_here_is_opening_line(self):
        text = "Here is the Introduction section:\n\nThe system provides..."
        result = sanitize_content(text)
        assert "Here is" not in result
        assert "The system provides" in result

    def test_removes_certainly_line(self):
        text = "Certainly! Here is the polished abstract:\n\nThe project addresses..."
        result = sanitize_content(text)
        assert "Certainly" not in result
        assert "The project addresses" in result

    def test_removes_let_me_know_closing(self):
        text = (
            "The implementation leverages asyncio for concurrency.\n\n"
            "Let me know if you need any changes."
        )
        result = sanitize_content(text)
        assert "Let me know" not in result
        assert "asyncio" in result

    def test_removes_hope_this_helps(self):
        text = "The system uses FastAPI.\n\nHope this helps!"
        result = sanitize_content(text)
        assert "Hope this helps" not in result
        assert "FastAPI" in result

    def test_removes_markdown_separators(self):
        text = "Section content.\n\n---\n\nMore content."
        result = sanitize_content(text)
        assert "---" not in result
        assert "Section content" in result
        assert "More content" in result

    def test_collapses_blank_lines(self):
        text = "Line one.\n\n\n\n\nLine two."
        result = sanitize_content(text)
        assert "\n\n\n" not in result

    def test_empty_input_returns_empty(self):
        assert sanitize_content("") == ""

    def test_only_chatter_returns_empty_or_minimal(self):
        text = "Here is the polished version of your section:\nLet me know if you need changes."
        result = sanitize_content(text)
        # All chatter should be stripped
        assert "Here is" not in result
        assert "Let me know" not in result

    def test_real_world_chatter_example(self):
        """Mirrors the actual LLM output pattern reported in the issue."""
        text = (
            "Here is the polished version of your Introduction section:\n\n"
            "The Dr. Document system is an AI-powered documentation generator designed "
            "to automate the creation of research papers, SRS documents, and GitHub "
            "community files from a repository URL.\n\n"
            "Let me know if you would like any adjustments."
        )
        result = sanitize_content(text)
        assert "Here is the polished version" not in result
        assert "Let me know" not in result
        assert "Dr. Document system" in result
        assert not has_meta_chatter(result)

    def test_content_with_banned_phrase_mid_document(self):
        """Ensure we do not over-strip legitimate mid-paragraph text."""
        text = (
            "The architecture below is described in detail in the system design section. "
            "As noted by the original authors, the pipeline was designed for extensibility."
        )
        # "below is" inside a sentence should NOT strip the whole sentence
        result = sanitize_content(text)
        # The important thing: the document content is preserved
        assert "pipeline was designed for extensibility" in result


# ---------------------------------------------------------------------------
# sanitize_content — control character stripping
# ---------------------------------------------------------------------------

class TestSanitizeContentControlChars:
    """Verify that null bytes and other LaTeX-invalid control characters are
    removed so they can never reach the .tex file."""

    def test_strips_null_bytes(self):
        text = "Error notifications\x00 with detailed messages"
        result = sanitize_content(text)
        assert '\x00' not in result
        assert "Error notifications" in result
        assert "with detailed messages" in result

    def test_strips_null_byte_only_string(self):
        assert sanitize_content("\x00") == ""

    def test_strips_multiple_null_bytes(self):
        text = "line one\x00\x00\nline two"
        result = sanitize_content(text)
        assert '\x00' not in result
        assert "line one" in result
        assert "line two" in result

    def test_strips_other_control_chars(self):
        """BEL, BS, VT, FF, SO, SI etc. must all be removed."""
        controls = "\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x1f\x7f"
        text = f"before{controls}after"
        result = sanitize_content(text)
        for ch in controls:
            assert ch not in result
        assert "before" in result
        assert "after" in result

    def test_preserves_newline_tab_cr(self):
        """Newline, tab and carriage return are valid and must be kept."""
        text = "line one\nline two\ttabbed\rcarriage"
        result = sanitize_content(text)
        assert "line one" in result
        assert "line two" in result

    def test_placeholder_lookalike_from_llm_null_bytes_removed(self):
        """If LLM somehow emits a SPAN-placeholder-like string with null bytes,
        those null bytes must be removed."""
        # Simulate LLM output that contains what looks like a leaked placeholder
        text = "feature\x00SPAN0\x00: Error notifications with detailed messages"
        result = sanitize_content(text)
        assert '\x00' not in result
        assert "Error notifications with detailed messages" in result
