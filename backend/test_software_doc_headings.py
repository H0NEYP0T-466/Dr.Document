"""Unit tests for SoftwareDocHeadingsAgent._parse_sections

Specifically verifies that all MANDATORY_HEADINGS are always present in the
returned sections list even when the LLM only emits a subset of them.

Run with:
    cd /path/to/Dr.Document
    python -m pytest backend/test_software_doc_headings.py -v
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from backend.agents.software_doc.headings_agent import (
    SoftwareDocHeadingsAgent,
    MANDATORY_HEADINGS,
)


def _parse(raw: str):
    """Helper: call _parse_sections without triggering the full __init__."""
    from unittest.mock import patch
    with patch.object(SoftwareDocHeadingsAgent, '__init__', return_value=None):
        agent = SoftwareDocHeadingsAgent()
    return agent._parse_sections(raw)


class TestParseSectionsAlwaysHasMandatoryHeadings:
    """All MANDATORY_HEADINGS must be present regardless of LLM output."""

    def _assert_mandatory_present(self, sections):
        names_lower = {s['name'].lower() for s in sections}
        for heading in MANDATORY_HEADINGS:
            assert heading.lower() in names_lower, (
                f"Mandatory heading '{heading}' missing from parsed sections"
            )

    def test_empty_llm_output_returns_all_mandatory(self):
        sections = _parse("")
        self._assert_mandatory_present(sections)

    def test_single_section_output_still_includes_all_mandatory(self):
        """Regression: previously only Declaration was returned when LLM emitted one section."""
        raw = (
            "SECTION_2: Declaration / Originality Statement\n"
            "BRIEF: This section declares the originality of the work.\n"
        )
        sections = _parse(raw)
        self._assert_mandatory_present(sections)
        assert len(sections) >= len(MANDATORY_HEADINGS)

    def test_partial_llm_output_supplemented(self):
        """A few parsed sections should still result in all mandatory headings."""
        raw = (
            "SECTION_1: Title Page\n"
            "BRIEF: The title page.\n\n"
            "SECTION_2: Declaration / Originality Statement\n"
            "BRIEF: Declare originality.\n\n"
            "SECTION_7: Introduction\n"
            "BRIEF: Introduces the project.\n"
        )
        sections = _parse(raw)
        self._assert_mandatory_present(sections)

    def test_full_output_preserved(self):
        """When LLM returns all mandatory headings they are all preserved."""
        lines = []
        for i, heading in enumerate(MANDATORY_HEADINGS, start=1):
            lines.append(f"SECTION_{i}: {heading}")
            lines.append(f"BRIEF: Write the {heading} section.")
            lines.append("")
        sections = _parse("\n".join(lines))
        self._assert_mandatory_present(sections)
        assert len(sections) == len(MANDATORY_HEADINGS)

    def test_mandatory_order_preserved(self):
        """Mandatory headings appear in MANDATORY_HEADINGS order."""
        raw = (
            "SECTION_1: Introduction\n"
            "BRIEF: Introduces the project.\n\n"
            "SECTION_2: Title Page\n"
            "BRIEF: Title page content.\n"
        )
        sections = _parse(raw)
        mandatory_lower = [h.lower() for h in MANDATORY_HEADINGS]
        returned_names = [s['name'].lower() for s in sections]
        # Verify ordering: for any two mandatory headings, their relative order
        # in the result must match MANDATORY_HEADINGS.
        for a, b in zip(mandatory_lower, mandatory_lower[1:]):
            idx_a = returned_names.index(a)
            idx_b = returned_names.index(b)
            assert idx_a < idx_b, (
                f"Heading '{a}' should come before '{b}' but order was wrong"
            )

    def test_optional_sections_appended_after_mandatory(self):
        """Optional sections emitted by the LLM appear after all mandatory headings."""
        raw = (
            "SECTION_1: Title Page\n"
            "BRIEF: Title.\n\n"
            "SECTION_2: API Reference\n"
            "BRIEF: Optional API docs.\n"
        )
        sections = _parse(raw)
        names = [s['name'] for s in sections]
        # API Reference is optional (not in MANDATORY_HEADINGS)
        api_idx = names.index("API Reference")
        # All mandatory headings should appear before the optional one
        for heading in MANDATORY_HEADINGS:
            mand_idx = names.index(heading)
            assert mand_idx < api_idx, (
                f"Mandatory heading '{heading}' should come before optional 'API Reference'"
            )

    def test_brief_preserved_for_llm_parsed_section(self):
        """LLM-supplied briefs are preserved; default brief used for supplemented ones."""
        raw = (
            "SECTION_7: Introduction\n"
            "BRIEF: This section provides project context and motivation.\n"
        )
        sections = _parse(raw)
        intro = next(s for s in sections if s['name'].lower() == 'introduction')
        assert intro['brief'] == "This section provides project context and motivation."

        abstract = next(s for s in sections if s['name'].lower() == 'abstract')
        assert abstract['brief'] == "Write the Abstract section."

    def test_sections_with_no_brief_still_included(self):
        """Sections emitted without a BRIEF: line are still captured."""
        raw = (
            "SECTION_1: Title Page\n"
            "SECTION_2: Abstract\n"
            "BRIEF: The abstract.\n"
        )
        sections = _parse(raw)
        names_lower = {s['name'].lower() for s in sections}
        assert 'title page' in names_lower
        assert 'abstract' in names_lower
