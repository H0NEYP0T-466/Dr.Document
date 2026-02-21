"""Agent 2: Headings Selector - Decides which documentation headings to include → headings.txt"""
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


# Predefined candidate headings (the agent may add others)
CANDIDATE_HEADINGS: List[str] = [
    "Abstract",
    "Key Highlights",
    "Dataset & Training Details",
    "Architecture",
    "Methodology",
    "Results & Visualizations",
    "Quick Start",
    "Features",
    "Project Structure",
    "Documentation",
    "API Endpoints",
    "Model Setup & Training",
    "Configuration",
    "Development",
    "Deployment",
    "Installation",
    "Usage",
    "Submodules",
    "Tech Stack",
    "Dependencies & Packages",
    "Prerequisites",
    "Contributing",
    "License",
    "Security",
    "Code of Conduct",
    "Citation",
    "Contact",
    "Acknowledgments",
]


class HeadingsSelectorAgent(BaseAgent):
    """
    Reads codebase.txt and selects the most relevant README headings for the project.
    The agent may also suggest additional headings beyond the candidate list.
    """

    def __init__(self):
        super().__init__("Headings Selector", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select relevant headings based on the codebase summary.

        Args:
            input_data: {
                'codebase_summary': str,  # content of codebase.txt
                'repo_name': str,
            }

        Returns:
            {
                'headings': List[str],
                'headings_txt': str,    # newline-separated for saving
            }
        """
        codebase_summary = input_data.get('codebase_summary', '')
        repo_name = input_data.get('repo_name', 'Unknown Repository')

        logger.workflow_step("Headings Selection", f"Selecting headings for {repo_name}")

        candidate_list = '\n'.join(f"- {h}" for h in CANDIDATE_HEADINGS)

        prompt = (
            f'You are deciding which documentation sections to include in a README for the '
            f'repository "{repo_name}".\n\n'
            f'Below is a concise summary of every file in the codebase:\n'
            f'{codebase_summary}\n\n'
            f'Here are candidate headings:\n{candidate_list}\n\n'
            f'Rules:\n'
            f'1. Only include headings that are relevant to this project '
            f'(e.g., "Dataset & Training Details" only if it is an ML/DL project).\n'
            f'2. You may suggest additional headings not in the list if the project needs them.\n'
            f'3. Return ONLY the list of selected headings, one per line, nothing else. '
            f'No numbering, no bullets, no explanations.'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a documentation architect. "
                    "Select the most relevant README sections for the given project."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        raw = self._call_llm(messages, max_tokens=512, temperature=0.3)

        # Parse headings — one per line, strip whitespace / bullet chars; deduplicate
        headings: List[str] = []
        seen: set = set()
        for line in raw.strip().split('\n'):
            heading = line.strip().lstrip('-•* 0123456789.')
            if heading and heading.lower() not in seen:
                headings.append(heading)
                seen.add(heading.lower())

        headings_txt = '\n'.join(headings)

        logger.success(f"Selected {len(headings)} headings for {repo_name}")
        logger.info(f"Headings: {headings}")

        return {
            'headings': headings,
            'headings_txt': headings_txt,
        }
