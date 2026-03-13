"""Software Documentation Headings Agent - Builds TOC for a software documentation report"""
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


MANDATORY_HEADINGS: List[str] = [
    "Title Page",
    "Declaration / Originality Statement",
    "Acknowledgements",
    "Abstract",
    "Table of Contents",
    "List of Abbreviations",
    "Introduction",
    "System Overview",
    "Requirements Analysis",
    "System Architecture & Design",
    "Implementation Details",
    "Testing & Validation",
    "Conclusion & Future Work",
    "References",
    "Appendices",
]

OPTIONAL_HEADING_CANDIDATES = [
    "Database Design",
    "API Reference",
    "Deployment Guide",
    "Security Analysis",
    "Performance Analysis",
    "User Manual",
    "List of Figures",
]


class SoftwareDocHeadingsAgent(BaseAgent):
    """
    Decides the full table of contents for the software documentation report.
    Mandatory headings are always included; optional ones are added based on the codebase.
    """

    def __init__(self):
        super().__init__("Software Doc Headings Agent", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select headings and write a brief for each section.

        Args:
            input_data: {
                'codebase_summary': str,
                'title_txt': str,
                'selected_title': str,
                'repo_name': str,
            }

        Returns:
            {
                'headings_txt': str,
                'sections': List[Dict],
            }
        """
        codebase_summary = input_data.get('codebase_summary', '')
        selected_title = input_data.get('selected_title', 'Software Documentation')
        repo_name = input_data.get('repo_name', 'Unknown Repository')

        logger.workflow_step("Software Doc Headings", f"Building TOC for {repo_name}")

        mandatory_list = '\n'.join(f"- {h}" for h in MANDATORY_HEADINGS)
        optional_list = '\n'.join(f"- {h}" for h in OPTIONAL_HEADING_CANDIDATES)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a technical documentation architect. "
                    "Build a complete table of contents for a software documentation report "
                    "and write a brief for each section."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Document title: {selected_title}\n"
                    f"Repository: {repo_name}\n\n"
                    f"Codebase Summary:\n{codebase_summary}\n\n"
                    f"MANDATORY sections (always include, in this order):\n"
                    f"{mandatory_list}\n\n"
                    f"OPTIONAL sections (include only if codebase warrants):\n"
                    f"{optional_list}\n\n"
                    f"For each section, write a one-paragraph BRIEF explaining "
                    f"what the section must cover, what evidence to draw from the codebase, "
                    f"and the expected tone (explanatory, less formal than a research paper).\n\n"
                    f"Output format:\n"
                    f"TITLE: [document title]\n"
                    f"TOTAL_SECTIONS: N\n\n"
                    f"SECTION_1: Title Page\n"
                    f"BRIEF: [writing brief]\n\n"
                    f"SECTION_2: Declaration / Originality Statement\n"
                    f"BRIEF: [writing brief]\n"
                    f"... and so on."
                ),
            },
        ]

        raw = self._call_llm(messages, max_tokens=2048, temperature=0.4)
        sections = self._parse_sections(raw)

        logger.success(f"Software doc TOC: {len(sections)} sections")

        return {
            'headings_txt': raw.strip(),
            'sections': sections,
        }

    def _parse_sections(self, raw: str) -> List[Dict[str, str]]:
        """Parse SECTION_N / BRIEF pairs from LLM output."""
        sections: List[Dict[str, str]] = []
        lines = raw.strip().splitlines()
        current_name = None
        current_brief_lines: List[str] = []

        for line in lines:
            stripped = line.strip()
            if stripped.upper().startswith('SECTION_') and ':' in stripped:
                if current_name:
                    sections.append({
                        'name': current_name,
                        'brief': ' '.join(current_brief_lines).strip(),
                    })
                    current_brief_lines = []
                current_name = stripped.split(':', 1)[1].strip()
            elif stripped.upper().startswith('BRIEF:') and current_name:
                current_brief_lines = [stripped.split(':', 1)[1].strip()]
            elif current_name and current_brief_lines and stripped:
                current_brief_lines.append(stripped)

        if current_name:
            sections.append({
                'name': current_name,
                'brief': ' '.join(current_brief_lines).strip(),
            })

        if not sections:
            sections = [{'name': h, 'brief': f'Write the {h} section.'} for h in MANDATORY_HEADINGS]

        return sections
