"""Research Paper Headings Agent - Decides the full table of contents for the research paper"""
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


MANDATORY_HEADINGS: List[str] = [
    "Abstract",
    "Introduction",
    "Related Work",
    "System Architecture / Methodology",
    "Implementation",
    "Results & Evaluation",
    "Discussion",
    "Conclusion",
    "References",
]


class ResearchPaperHeadingsAgent(BaseAgent):
    """
    Decides the full table of contents for the research paper.
    Mandatory headings are always included; optional ones are added
    based on what the codebase warrants.
    """

    def __init__(self):
        super().__init__("Research Paper Headings Agent", settings.model_flash_lite)

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
                'headings_txt': str,  # structured headings.txt content
                'sections': List[Dict],  # [{name, brief}, ...]
            }
        """
        codebase_summary = input_data.get('codebase_summary', '')
        selected_title = input_data.get('selected_title', 'Research Paper')
        repo_name = input_data.get('repo_name', 'Unknown Repository')

        logger.workflow_step("Research Paper Headings", f"Building TOC for {repo_name}")

        mandatory_list = '\n'.join(f"- {h}" for h in MANDATORY_HEADINGS)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an academic paper architect. "
                    "Build a complete table of contents for a research paper "
                    "and write a brief for each section."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Paper title: {selected_title}\n"
                    f"Repository: {repo_name}\n\n"
                    f"Codebase Summary:\n{codebase_summary}\n\n"
                    f"MANDATORY sections (always include, in this order):\n"
                    f"{mandatory_list}\n\n"
                    f"After analyzing the codebase, add OPTIONAL sections only if "
                    f"genuinely warranted (e.g. 'Dataset Description', 'API Design', "
                    f"'Security Analysis', 'Performance Benchmarks', 'Limitations', "
                    f"'Future Work'). Insert them in a logical position.\n\n"
                    f"For each section, write a one-paragraph BRIEF explaining "
                    f"what the section agent must cover, what evidence to draw from "
                    f"the codebase, and the expected tone and depth.\n\n"
                    f"Output format:\n"
                    f"TITLE: [paper title]\n"
                    f"TOTAL_SECTIONS: N\n\n"
                    f"SECTION_1: Abstract\n"
                    f"BRIEF: [writing brief]\n\n"
                    f"SECTION_2: Introduction\n"
                    f"BRIEF: [writing brief]\n"
                    f"... and so on for all sections."
                ),
            },
        ]

        raw = self._call_llm(messages, max_tokens=2048, temperature=0.4)

        # Parse sections
        sections = self._parse_sections(raw)

        logger.success(f"Research paper TOC: {len(sections)} sections")

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
                # Save previous
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
                # Continuation of the brief
                current_brief_lines.append(stripped)

        if current_name:
            sections.append({
                'name': current_name,
                'brief': ' '.join(current_brief_lines).strip(),
            })

        # If parsing failed, fall back to mandatory headings
        if not sections:
            sections = [{'name': h, 'brief': f'Write the {h} section.'} for h in MANDATORY_HEADINGS]

        return sections
