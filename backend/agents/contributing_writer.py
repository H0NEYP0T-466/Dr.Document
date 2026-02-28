"""Contributing Writer Agent - Generates a CONTRIBUTING.md file"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class ContributingWriterAgent(BaseAgent):
    """Writes a CONTRIBUTING.md file based on latest standards."""

    def __init__(self):
        super().__init__("Contributing Writer", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a CONTRIBUTING.md file.

        Args:
            input_data: {
                'repo_name': str,
                'repo_owner': str,
                'codebase_summary': str,
                'improvement_notes': str,  (optional)
            }

        Returns:
            {
                'filename': 'CONTRIBUTING.md',
                'content': str,
            }
        """
        repo_name = input_data.get('repo_name', 'this repository')
        repo_owner = input_data.get('repo_owner', '')
        codebase_summary = input_data.get('codebase_summary', '')
        improvement_notes = input_data.get('improvement_notes', '')

        logger.workflow_step("Contributing Writer", f"Generating CONTRIBUTING.md for {repo_name}")

        improvement_block = ''
        if improvement_notes:
            improvement_block = (
                f'\n\nIMPROVEMENT NOTES (address ALL of these):\n{improvement_notes}'
            )

        prompt = (
            f'Write a comprehensive CONTRIBUTING.md for the GitHub repository "{repo_name}" '
            f'owned by "{repo_owner}".\n\n'
            f'CODEBASE CONTEXT (use to tailor the guide):\n{codebase_summary}\n\n'
            f'Follow the latest GitHub community standards. Include:\n'
            f'- Welcome message and how to get started\n'
            f'- How to report bugs (issue templates, expected info)\n'
            f'- How to suggest features / enhancements\n'
            f'- Pull request process (fork, branch naming, PR description)\n'
            f'- Code style and quality expectations\n'
            f'- Running tests / linting\n'
            f'- Code of Conduct reference\n'
            f'- Recognition / attribution\n\n'
            f'Start with "# Contributing to {repo_name}". Use proper Markdown with emojis '
            f'where appropriate. Be friendly and welcoming.'
            f'{improvement_block}'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert open-source maintainer writing contribution guidelines. "
                    "Follow the latest GitHub community standards."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        content = self._call_llm(messages, max_tokens=1500, temperature=0.5)
        content = content.strip()

        logger.success(f"CONTRIBUTING.md generated ({len(content)} chars)")

        return {
            'filename': 'CONTRIBUTING.md',
            'content': content,
        }
