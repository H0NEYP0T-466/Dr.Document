"""Title Agent - Proposes and selects a formal title for any document mode"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class TitleAgent(BaseAgent):
    """
    Reads codebase_summary.txt and proposes 3 candidate titles,
    then selects the best one and justifies the choice.

    Output: title.txt
    """

    def __init__(self):
        super().__init__("Title Agent", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Propose and select a title.

        Args:
            input_data: {
                'codebase_summary': str,
                'repo_name': str,
            }

        Returns:
            {
                'title_txt': str,       # full content for title.txt
                'selected_title': str,  # just the chosen title
            }
        """
        codebase_summary = input_data.get('codebase_summary', '')
        repo_name = input_data.get('repo_name', 'Unknown Repository')

        logger.workflow_step("Title Agent", f"Generating title for {repo_name}")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an academic title generator. "
                    "Propose exactly 3 candidate titles for a formal document about "
                    "the described software project, then select the best one."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Repository: {repo_name}\n\n"
                    f"Codebase Summary:\n{codebase_summary}\n\n"
                    f"Generate 3 formal academic titles for this project. "
                    f"Titles must be descriptive and in formal academic style, "
                    f"e.g. 'A Multi-Agent Framework for Automated GitHub Repository "
                    f"Documentation Using Large Language Models'.\n\n"
                    f"Output format (follow exactly):\n"
                    f"CANDIDATE_1: [title]\n"
                    f"CANDIDATE_2: [title]\n"
                    f"CANDIDATE_3: [title]\n"
                    f"SELECTED: CANDIDATE_[N]\n"
                    f"SELECTED_TITLE: [exact text of selected title]\n"
                    f"JUSTIFICATION: [one sentence explaining why this title is best]"
                ),
            },
        ]

        raw = self._call_llm(messages, max_tokens=512, temperature=0.5)

        # Extract the selected title
        selected_title = repo_name  # fallback
        for line in raw.strip().splitlines():
            if line.upper().startswith('SELECTED_TITLE:'):
                selected_title = line.split(':', 1)[1].strip()
                break

        logger.success(f"Title selected: {selected_title}")

        return {
            'title_txt': raw.strip(),
            'selected_title': selected_title,
        }
