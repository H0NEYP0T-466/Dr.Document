"""SRS Headings Agent - Builds IEEE 830 compliant table of contents"""
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


# IEEE 830 mandatory structure (strict order)
MANDATORY_HEADINGS: List[str] = [
    "Title Page",
    "Table of Contents",
    "Introduction",
    "1.1 Purpose",
    "1.2 Scope",
    "1.3 Definitions, Acronyms, and Abbreviations",
    "1.4 References",
    "1.5 Overview",
    "Overall Description",
    "2.1 Product Perspective",
    "2.2 Product Functions",
    "2.3 User Classes and Characteristics",
    "2.4 Operating Environment",
    "2.5 Design and Implementation Constraints",
    "2.6 Assumptions and Dependencies",
    "System Features",
    "External Interface Requirements",
    "4.1 User Interfaces",
    "4.2 Hardware Interfaces",
    "4.3 Software Interfaces",
    "4.4 Communication Interfaces",
    "Non-Functional Requirements",
    "5.1 Performance Requirements",
    "5.2 Safety Requirements",
    "5.3 Security Requirements",
    "5.4 Software Quality Attributes",
    "Other Requirements",
    "Appendix A: Glossary",
    "Appendix B: Analysis Models",
]


class SRSHeadingsAgent(BaseAgent):
    """
    Builds the IEEE 830 SRS table of contents.
    Also detects system features from the codebase summary to populate Section 3.
    """

    def __init__(self):
        super().__init__("SRS Headings Agent", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build the IEEE 830 TOC and detect system features.

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
                'system_features': List[str],
            }
        """
        codebase_summary = input_data.get('codebase_summary', '')
        selected_title = input_data.get('selected_title', 'Software Requirements Specification')
        repo_name = input_data.get('repo_name', 'Unknown Repository')

        logger.workflow_step("SRS Headings", f"Building IEEE 830 TOC for {repo_name}")

        mandatory_list = '\n'.join(f"- {h}" for h in MANDATORY_HEADINGS)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an IEEE 830 SRS architect. "
                    "Build a complete SRS table of contents strictly following IEEE 830, "
                    "detect system features from the codebase, and write a brief for each section."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Document title: {selected_title}\n"
                    f"Repository: {repo_name}\n\n"
                    f"Codebase Summary:\n{codebase_summary}\n\n"
                    f"MANDATORY sections per IEEE 830 (strict order, do not reorder):\n"
                    f"{mandatory_list}\n\n"
                    f"For Section 3 (System Features): detect ALL major features from the "
                    f"codebase summary. List each as a subsection: "
                    f"'3.1 [Feature Name]', '3.2 [Feature Name]', etc.\n\n"
                    f"For each section and subsection, write a BRIEF explaining what must be "
                    f"covered (declarative SRS language: 'shall', 'should', 'may').\n\n"
                    f"Also list detected features:\n"
                    f"DETECTED_FEATURES: feature1, feature2, ...\n\n"
                    f"Output format:\n"
                    f"TITLE: [document title]\n"
                    f"DETECTED_FEATURES: [comma-separated list]\n"
                    f"TOTAL_SECTIONS: N\n\n"
                    f"SECTION_1: Title Page\n"
                    f"BRIEF: [brief]\n\n"
                    f"SECTION_2: Table of Contents\n"
                    f"BRIEF: [brief]\n"
                    f"... etc."
                ),
            },
        ]

        raw = self._call_llm(messages, max_tokens=2048, temperature=0.4)
        sections = self._parse_sections(raw)
        features = self._parse_features(raw)

        logger.success(f"SRS TOC: {len(sections)} sections, {len(features)} features detected")

        return {
            'headings_txt': raw.strip(),
            'sections': sections,
            'system_features': features,
        }

    def _parse_sections(self, raw: str) -> List[Dict[str, str]]:
        """Parse SECTION_N / BRIEF pairs."""
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
                if not stripped.upper().startswith('SECTION_'):
                    current_brief_lines.append(stripped)

        if current_name:
