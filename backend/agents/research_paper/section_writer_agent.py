"""Research Paper Section Writer Agent - Writes one section of the research paper"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class ResearchPaperSectionWriterAgent(BaseAgent):
    """
    Writes a single section of the research paper based on the brief
    from the headings agent and the codebase summary.
    """

    def __init__(self, section_name: str):
        safe = section_name.replace(' ', '_').replace('/', '_')[:40]
        super().__init__(f"Section Writer [{section_name}]", settings.model_flash_lite)
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
                'manager_feedback': str,   # provided on restart
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

        logger.workflow_step("Research Paper Section", f"Writing '{section_name}'")

        # Build feedback block for restarts
        feedback_block = ''
        if manager_feedback:
            feedback_block = (
                f'\n\nMANAGER FEEDBACK (address ALL of these points):\n{manager_feedback}'
            )

        # Special rules for specific sections
        section_rules = self._get_section_rules(section_name)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert academic researcher and technical writer. "
                    "Write formal, high-quality research paper sections in academic English. "
                    "Never fabricate — only write what can be inferred from the codebase."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Paper title: {selected_title}\n"
                    f"Repository: {repo_name}\n\n"
                    f"Full table of contents:\n{headings_txt}\n\n"
                    f"Codebase Summary:\n{codebase_summary}\n\n"
                    f"Your task: Write ONLY the '{section_name}' section.\n\n"
                    f"Section Brief:\n{section_brief}\n\n"
                    f"Rules:\n"
                    f"- Use formal academic English throughout\n"
                    f"- No casual language, no bullet points except where explicitly appropriate\n"
                    f"- Only write what can be inferred from the codebase summary\n"
                    f"- If information is unavailable: write "
                    f"'Not determinable from repository analysis.'\n"
                    f"- Cite relevant files from the codebase summary as evidence\n"
                    f"{section_rules}"
                    f"{feedback_block}"
                ),
            },
        ]

        content = self._call_llm(messages, max_tokens=1500, temperature=0.5)
        content = content.strip()
        word_count = len(content.split())

        logger.success(f"Wrote '{section_name}' ({word_count} words)")

        return {
            'section_name': section_name,
            'content': content,
            'word_count': word_count,
        }

    def _get_section_rules(self, section_name: str) -> str:
        """Return section-specific writing rules."""
        lower = section_name.lower()
        if lower == 'abstract':
            return (
                '- Abstract: 150-250 words, structured as: '
                'problem statement, approach, results, conclusion\n'
                '- Do NOT use first person ("we", "our")\n'
            )
        if lower == 'references':
            return (
                '- Use IEEE citation format: [1] Author, "Title," Journal, year.\n'
                '- Cite: GitHub repo URL, key libraries with their docs URLs, '
                'any papers referenced in README or code comments\n'
                '- Format as a numbered list\n'
            )
        return (
            '- Minimum 300 words\n'
            '- Use \\section{} heading style in prose\n'
        )
