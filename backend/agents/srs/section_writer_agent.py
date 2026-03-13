"""SRS Section Writer Agent - Writes IEEE 830 compliant SRS sections"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class SRSSectionWriterAgent(BaseAgent):
    """
    Writes a single section of the Software Requirements Specification.
    Strictly follows IEEE 830 declarative language rules.
    """

    def __init__(self, section_name: str):
        super().__init__(f"SRS Section Writer [{section_name}]", settings.model_flash_lite)
        self.section_name = section_name

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Write the assigned SRS section.

        Args:
            input_data: {
                'section_name': str,
                'section_brief': str,
                'codebase_summary': str,
                'headings_txt': str,
                'selected_title': str,
                'repo_name': str,
                'system_features': List[str],
                'manager_feedback': str,
            }

        Returns:
            {
                'section_name': str,
                'content': str,
                'word_count': int,
            }
        """
        section_name = input_data.get('section_name', self.section_name)
        section_brief = input_data.get('section_brief', '')
        codebase_summary = input_data.get('codebase_summary', '')
        headings_txt = input_data.get('headings_txt', '')
        selected_title = input_data.get('selected_title', '')
        repo_name = input_data.get('repo_name', '')
        system_features = input_data.get('system_features', [])
        manager_feedback = input_data.get('manager_feedback', '')

        logger.workflow_step("SRS Section", f"Writing '{section_name}'")

        feedback_block = ''
        if manager_feedback:
            feedback_block = (
                f'\n\nMANAGER FEEDBACK (address ALL of these):\n{manager_feedback}'
            )

        features_context = ''
        if system_features:
            features_context = (
                f'\nDetected system features: {", ".join(system_features)}\n'
            )

        # Determine if this is a system features section
        is_features_section = 'system feature' in section_name.lower() or (
            section_name.startswith('3.') and section_name[2:3].isdigit()
        )

        feature_rules = ''
        if is_features_section:
            feature_rules = (
                '\nFor this System Feature section include:\n'
                '- Description and priority (High/Medium/Low)\n'
                '- Stimulus/Response sequence\n'
                '- At minimum 3 functional requirements using format:\n'
                '  FR-[section]-[number]: The system shall...\n'
                '  e.g. FR-3.1-001: The system shall process repository URLs within 30 seconds.\n'
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an IEEE 830 SRS technical writer. "
                    "Write declarative, precise SRS sections. "
                    "Use 'shall' for mandatory requirements, 'should' for desired, 'may' for optional. "
                    "No opinions, no evaluative language. Never fabricate."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"SRS title: {selected_title}\n"
                    f"Repository: {repo_name}\n"
                    f"{features_context}\n"
                    f"Full TOC:\n{headings_txt}\n\n"
                    f"Codebase Summary:\n{codebase_summary}\n\n"
                    f"Write ONLY the '{section_name}' section.\n\n"
                    f"Section Brief:\n{section_brief}\n\n"
                    f"SRS Writing Rules:\n"
                    f"- Declarative language only (no 'we plan to', no 'the system tries to')\n"
                    f"- Use 'shall' for mandatory, 'should' for desired, 'may' for optional\n"
                    f"- If information unavailable: "
                    f"'Not determinable from repository analysis.'\n"
                    f"- Non-functional requirements: NFR-[category]-[number]: The system shall...\n"
                    f"{feature_rules}"
                    f"{feedback_block}"
                ),
            },
        ]

        content = self._call_llm(messages, max_tokens=1500, temperature=0.4)
        content = content.strip()
        word_count = len(content.split())

        logger.success(f"Wrote SRS section '{section_name}' ({word_count} words)")

        return {
            'section_name': section_name,
            'content': content,
            'word_count': word_count,
        }
