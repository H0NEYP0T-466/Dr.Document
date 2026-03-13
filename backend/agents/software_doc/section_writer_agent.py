"""Software Documentation Section Writer Agent"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class SoftwareDocSectionWriterAgent(BaseAgent):
    """
    Writes a single section of the software documentation report.
    Tone is explanatory rather than argumentative (less formal than a research paper).
    """

    def __init__(self, section_name: str):
        super().__init__(f"Software Doc Section Writer [{section_name}]", settings.model_flash_lite)
        self.section_name = section_name

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Write the assigned section.

        Args:
            input_data: {
                'section_name': str,
                'section_brief': str,
                'codebase_summary': str,
                'headings_txt': str,
                'selected_title': str,
                'repo_name': str,
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
        manager_feedback = input_data.get('manager_feedback', '')

        logger.workflow_step("Software Doc Section", f"Writing '{section_name}'")

        feedback_block = ''
        if manager_feedback:
            feedback_block = (
                f'\n\nMANAGER FEEDBACK (address ALL of these points):\n{manager_feedback}'
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert technical documentation writer. "
                    "Write clear, explanatory software documentation sections. "
                    "The tone should be professional but accessible — explain what the system "
                    "does and how it works. Never fabricate."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Document title: {selected_title}\n"
                    f"Repository: {repo_name}\n\n"
                    f"Full table of contents:\n{headings_txt}\n\n"
                    f"Codebase Summary:\n{codebase_summary}\n\n"
                    f"Your task: Write ONLY the '{section_name}' section.\n\n"
                    f"Section Brief:\n{section_brief}\n\n"
                    f"Rules:\n"
                    f"- Professional but explanatory tone (not argumentative)\n"
                    f"- Only mention what can be inferred from the codebase summary\n"
                    f"- If information is unavailable: write "
                    f"'Not determinable from repository analysis.'\n"
                    f"- Minimum 200 words for substantive sections\n"
                    f"- Use headings and sub-headings where appropriate\n"
                    f"{feedback_block}"
                ),
            },
        ]

        content = self._call_llm(messages, max_tokens=1500, temperature=0.5)
        content = content.strip()
        word_count = len(content.split())

        logger.success(f"Wrote software doc section '{section_name}' ({word_count} words)")

        return {
            'section_name': section_name,
            'content': content,
            'word_count': word_count,
        }
