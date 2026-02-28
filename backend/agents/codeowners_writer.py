"""Codeowners Writer Agent - Generates a CODEOWNERS file"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class CodeownersWriterAgent(BaseAgent):
    """Writes a CODEOWNERS file for the repository."""

    def __init__(self):
        super().__init__("Codeowners Writer", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a CODEOWNERS file.

        Args:
            input_data: {
                'repo_name': str,
                'repo_owner': str,
                'codebase_summary': str,
                'improvement_notes': str,  (optional)
            }

        Returns:
            {
                'filename': 'CODEOWNERS',
                'content': str,
            }
        """
        repo_name = input_data.get('repo_name', 'this repository')
        repo_owner = input_data.get('repo_owner', '')
        codebase_summary = input_data.get('codebase_summary', '')
        improvement_notes = input_data.get('improvement_notes', '')

        logger.workflow_step("Codeowners Writer", f"Generating CODEOWNERS for {repo_name}")

        improvement_block = ''
        if improvement_notes:
            improvement_block = (
                f'\n\nIMPROVEMENT NOTES (address ALL of these):\n{improvement_notes}'
            )

        prompt = (
            f'Write a CODEOWNERS file for the GitHub repository "{repo_name}" '
            f'owned by "@{repo_owner}".\n\n'
            f'CODEBASE CONTEXT (use to determine directory structure):\n{codebase_summary}\n\n'
            f'Rules:\n'
            f'- The default owner for all files must be "@{repo_owner}"\n'
            f'- If the codebase has distinct areas (e.g. backend/, frontend/, docs/), '
            f'add specific ownership rules for those paths\n'
            f'- Use glob patterns following GitHub CODEOWNERS syntax\n'
            f'- Add brief comments explaining each section\n\n'
            f'Output ONLY the raw CODEOWNERS file content — no markdown fences, no extra text. '
            f'Start with a comment line "# CODEOWNERS".'
            f'{improvement_block}'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a DevOps engineer writing a GitHub CODEOWNERS file. "
                    "Follow the exact GitHub CODEOWNERS syntax."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        content = self._call_llm(messages, max_tokens=512, temperature=0.2)
        content = content.strip()

        logger.success(f"CODEOWNERS generated ({len(content)} chars)")

        return {
            'filename': 'CODEOWNERS',
            'content': content,
        }
