"""Agent 1: Codebase Summarizer - Creates concise per-file summaries → codebase.txt"""
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class CodebaseSummarizerAgent(BaseAgent):
    """
    Reads each repository file one at a time and produces a single-line summary.
    Output is written to codebase.txt in the format:
        filename = what this file implements / features
    """

    def __init__(self):
        super().__init__("Codebase Summarizer", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize a single file.

        Args:
            input_data: {
                'file_path': str,
                'file_content': str,
            }

        Returns:
            {
                'file_path': str,
                'summary': str,  # one-line description
            }
        """
        file_path = input_data.get('file_path', 'unknown')
        file_content = input_data.get('file_content', '')

        logger.file_process(file_path, 'Summarizing')

        if not file_content.strip():
            return {'file_path': file_path, 'summary': 'Empty file'}

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a codebase analyst. For the given file, output a single short sentence "
                    "describing what the file implements, its main features, or its purpose. "
                    "Be extremely concise — one sentence max. "
                    "Do NOT include the filename in your response."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"File: {file_path}\n\n"
                    f"```\n{file_content[:4000]}\n```"
                ),
            },
        ]

        summary = self._call_llm(messages, max_tokens=200, temperature=0.3)
        summary = summary.strip().replace('\n', ' ')

        return {'file_path': file_path, 'summary': summary}

    def summarize_all(self, files_data: List[Dict]) -> str:
        """
        Summarize every file and return the complete codebase.txt content.

        Args:
            files_data: list of {'file_path': str, 'file_content': str}

        Returns:
            codebase.txt content as a string
        """
        lines = []
        for file_data in files_data:
            result = self.run(file_data)
            lines.append(f"{result['file_path']} = {result['summary']}")
        return '\n'.join(lines)
