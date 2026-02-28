"""Code of Conduct Writer Agent - Generates a CODE_OF_CONDUCT.md file"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class CodeOfConductWriterAgent(BaseAgent):
    """Writes a CODE_OF_CONDUCT.md following the Contributor Covenant v2.1."""

    def __init__(self):
        super().__init__("Code of Conduct Writer", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a CODE_OF_CONDUCT.md file.

        Args:
            input_data: {
                'repo_name': str,
                'repo_owner': str,
                'codebase_summary': str,
                'improvement_notes': str,  (optional)
            }

        Returns:
            {
                'filename': 'CODE_OF_CONDUCT.md',
                'content': str,
            }
        """
        repo_name = input_data.get('repo_name', 'this repository')
        repo_owner = input_data.get('repo_owner', '')
        improvement_notes = input_data.get('improvement_notes', '')

        logger.workflow_step("Code of Conduct Writer", f"Generating CODE_OF_CONDUCT.md for {repo_name}")

        improvement_block = ''
        if improvement_notes:
            improvement_block = (
                f'\n\nIMPROVEMENT NOTES (address ALL of these):\n{improvement_notes}'
            )

        prompt = (
            f'Write a CODE_OF_CONDUCT.md for the GitHub repository "{repo_name}" '
            f'owned by "{repo_owner}".\n\n'
            f'Base it on the Contributor Covenant v2.1 (the latest standard). Include:\n'
            f'- Our Pledge\n'
            f'- Our Standards (positive and unacceptable behaviour)\n'
            f'- Enforcement Responsibilities\n'
            f'- Scope\n'
            f'- Enforcement (how to report, consequences)\n'
            f'- Attribution (Contributor Covenant credit)\n\n'
            f'Use "{repo_owner}" as the contact for enforcement reports. '
            f'Start with "# Contributor Covenant Code of Conduct". '
            f'Output proper Markdown.'
            f'{improvement_block}'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert community manager writing a Code of Conduct "
                    "following the Contributor Covenant v2.1 standard."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        content = self._call_llm(messages, max_tokens=1500, temperature=0.3)
        content = content.strip()

        logger.success(f"CODE_OF_CONDUCT.md generated ({len(content)} chars)")

        return {
            'filename': 'CODE_OF_CONDUCT.md',
            'content': content,
        }
