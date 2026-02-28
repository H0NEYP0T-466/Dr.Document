"""License Writer Agent - Generates a MIT LICENSE file"""
from datetime import datetime
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class LicenseWriterAgent(BaseAgent):
    """Writes an MIT LICENSE file for the repository."""

    def __init__(self):
        super().__init__("License Writer", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an MIT LICENSE file.

        Args:
            input_data: {
                'repo_name': str,
                'repo_owner': str,
                'codebase_summary': str,   (optional context)
                'improvement_notes': str,  (optional)
            }

        Returns:
            {
                'filename': 'LICENSE',
                'content': str,
            }
        """
        repo_owner = input_data.get('repo_owner', 'The Authors')
        year = datetime.now().year
        improvement_notes = input_data.get('improvement_notes', '')

        logger.workflow_step("License Writer", f"Generating MIT LICENSE for {repo_owner}")

        improvement_block = ''
        if improvement_notes:
            improvement_block = (
                f'\n\nIMPROVEMENT NOTES (address ALL of these):\n{improvement_notes}'
            )

        prompt = (
            f'Generate a standard MIT License file for the year {year} with copyright holder '
            f'"{repo_owner}".\n\n'
            f'Output ONLY the raw license text — no markdown fences, no extra commentary, '
            f'no headings. Start directly with "MIT License".'
            f'{improvement_block}'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a legal documentation assistant. "
                    "Output the exact standard MIT License text."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        content = self._call_llm(messages, max_tokens=512, temperature=0.1)
        content = content.strip()

        logger.success(f"LICENSE generated ({len(content)} chars)")

        return {
            'filename': 'LICENSE',
            'content': content,
        }
