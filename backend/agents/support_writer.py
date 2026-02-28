"""Support Writer Agent - Generates a SUPPORT.md file"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class SupportWriterAgent(BaseAgent):
    """Writes a SUPPORT.md file following latest GitHub community standards."""

    def __init__(self):
        super().__init__("Support Writer", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a SUPPORT.md file.

        Args:
            input_data: {
                'repo_name': str,
                'repo_owner': str,
                'codebase_summary': str,
                'improvement_notes': str,  (optional)
            }

        Returns:
            {
                'filename': 'SUPPORT.md',
                'content': str,
            }
        """
        repo_name = input_data.get('repo_name', 'this repository')
        repo_owner = input_data.get('repo_owner', '')
        codebase_summary = input_data.get('codebase_summary', '')
        improvement_notes = input_data.get('improvement_notes', '')

        logger.workflow_step("Support Writer", f"Generating SUPPORT.md for {repo_name}")

        improvement_block = ''
        if improvement_notes:
            improvement_block = (
                f'\n\nIMPROVEMENT NOTES (address ALL of these):\n{improvement_notes}'
            )

        prompt = (
            f'Write a SUPPORT.md support guide for the GitHub repository "{repo_name}" '
            f'owned by "{repo_owner}".\n\n'
            f'CODEBASE CONTEXT (use to tailor the guide):\n{codebase_summary}\n\n'
            f'Follow the latest GitHub community health file standards. Include:\n'
            f'- Introduction (what support channels are available)\n'
            f'- GitHub Issues (when to use, what to include)\n'
            f'- GitHub Discussions (for questions and community help)\n'
            f'- Documentation links\n'
            f'- How to ask a good question\n'
            f'- What NOT to use issues for (e.g. general questions)\n'
            f'- Response time expectations\n\n'
            f'Start with "# Getting Support for {repo_name}". Output proper Markdown with emojis.'
            f'{improvement_block}'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert open-source maintainer writing a support guide "
                    "following the latest GitHub community standards."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        content = self._call_llm(messages, max_tokens=1200, temperature=0.5)
        content = content.strip()

        logger.success(f"SUPPORT.md generated ({len(content)} chars)")

        return {
            'filename': 'SUPPORT.md',
            'content': content,
        }
