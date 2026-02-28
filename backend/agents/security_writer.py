"""Security Writer Agent - Generates a SECURITY.md file"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class SecurityWriterAgent(BaseAgent):
    """Writes a SECURITY.md security policy following latest GitHub standards."""

    def __init__(self):
        super().__init__("Security Writer", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a SECURITY.md file.

        Args:
            input_data: {
                'repo_name': str,
                'repo_owner': str,
                'codebase_summary': str,
                'improvement_notes': str,  (optional)
            }

        Returns:
            {
                'filename': 'SECURITY.md',
                'content': str,
            }
        """
        repo_name = input_data.get('repo_name', 'this repository')
        repo_owner = input_data.get('repo_owner', '')
        codebase_summary = input_data.get('codebase_summary', '')
        improvement_notes = input_data.get('improvement_notes', '')

        logger.workflow_step("Security Writer", f"Generating SECURITY.md for {repo_name}")

        improvement_block = ''
        if improvement_notes:
            improvement_block = (
                f'\n\nIMPROVEMENT NOTES (address ALL of these):\n{improvement_notes}'
            )

        prompt = (
            f'Write a SECURITY.md security policy for the GitHub repository "{repo_name}" '
            f'owned by "{repo_owner}".\n\n'
            f'CODEBASE CONTEXT:\n{codebase_summary}\n\n'
            f'Follow the latest GitHub security policy standards. Include:\n'
            f'- Supported Versions (table showing which versions receive security updates)\n'
            f'- Reporting a Vulnerability (clear instructions on how to privately report)\n'
            f'- Disclosure Policy (responsible disclosure timeline)\n'
            f'- Security Response Process (what happens after a report)\n'
            f'- Out of Scope (what is NOT considered a vulnerability)\n'
            f'- Security Best Practices (brief tips for users)\n\n'
            f'Use GitHub private vulnerability reporting as the preferred channel. '
            f'Start with "# Security Policy". Output proper Markdown.'
            f'{improvement_block}'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a security expert writing a responsible disclosure policy "
                    "following the latest GitHub security standards."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        content = self._call_llm(messages, max_tokens=1200, temperature=0.4)
        content = content.strip()

        logger.success(f"SECURITY.md generated ({len(content)} chars)")

        return {
            'filename': 'SECURITY.md',
            'content': content,
        }
