"""Section Writer Agent - Writes a single README section based on codebase context"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger

# Headings that must render their content as shields.io badges
BADGE_HEADINGS = {
    "tech stack",
    "prerequisites",
}

# Headings that must keep code examples brief and minimal
MINIMAL_CODE_HEADINGS = {
    "quick start",
    "development",
    "deployment",
}


class SectionWriterAgent(BaseAgent):
    """
    Writes one specific README section.
    One instance is created per heading in the headings list.
    """

    def __init__(self, heading: str):
        safe_name = heading.replace(' ', '_').replace('&', 'and')[:40]
        super().__init__(f"Section Writer [{heading}]", settings.model_flash_lite)
        self.heading = heading

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Write a specific README section.

        Args:
            input_data: {
                'heading': str,
                'codebase_summary': str,
                'repo_name': str,
                'improvement_notes': str   (optional — provided on retries)
            }

        Returns:
            {
                'heading': str,
                'content': str,   # Markdown content for this section
            }
        """
        heading = input_data.get('heading', self.heading)
        codebase_summary = input_data.get('codebase_summary', '')
        repo_name = input_data.get('repo_name', 'Unknown Repository')
        improvement_notes = input_data.get('improvement_notes', '')

        logger.workflow_step("Section Writing", f"Writing '{heading}' for {repo_name}")

        # Build optional improvement block (for retries)
        improvement_block = ''
        if improvement_notes:
            improvement_block = (
                f'\n\nIMPROVEMENT NOTES FROM MANAGER (address ALL of these):\n'
                f'{improvement_notes}'
            )

        # Badge instruction for tech / dependency sections
        badge_instruction = ''
        if heading.lower() in BADGE_HEADINGS:
            extra = (
                ' Also include any critical third-party dependencies or packages as badges '
                '(e.g. key libraries, frameworks, or tools the project depends on).'
                if heading.lower() == 'tech stack'
                else ''
            )
            badge_instruction = (
                '\n\nIMPORTANT: Render every technology / package / tool as a shields.io badge '
                'using this exact format:\n'
                '<img src="https://img.shields.io/badge/{NAME}-{HEX_COLOR}?style=for-the-badge'
                '&logo={LOGO_SLUG}&logoColor=white" alt="{NAME}">\n'
                'Group related badges inside <p> tags. '
                'Use hex colours from simpleicons.org '
                '(e.g. Python=3776AB, React=61DAFB, FastAPI=009688, Docker=2496ED, '
                f'PostgreSQL=4169E1, TypeScript=3178C6, Node.js=339933).{extra}'
            )

        # Minimal-code instruction for quickstart / development / deployment
        minimal_code_instruction = ''
        if heading.lower() in MINIMAL_CODE_HEADINGS:
            minimal_code_instruction = (
                '\n\nIMPORTANT: Keep code examples minimal. '
                'Show only the essential commands needed to get started. '
                'Do NOT include exhaustive configuration files, long scripts, or '
                'step-by-step code blocks. Use short, focused snippets only.'
            )

        prompt = (
            f'You are writing the **{heading}** section for the README of the '
            f'repository "{repo_name}".\n\n'
            f'Here is a concise summary of every file in the codebase '
            f'(use this as your primary context):\n'
            f'{codebase_summary}\n\n'
            f'Write ONLY the content for the "{heading}" section. '
            f'Start directly with the markdown heading (e.g., ## {heading}).\n'
            f'Be thorough, accurate, and professional. '
            f'Use proper Markdown formatting with emojis where appropriate.\n'
            f'Do NOT include any other sections — only "{heading}".'
            f'{badge_instruction}'
            f'{minimal_code_instruction}'
            f'{improvement_block}'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert technical writer. "
                    "Write clear, accurate, and engaging documentation sections "
                    "based on the provided codebase analysis."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        content = self._call_llm(messages, max_tokens=2048, temperature=0.5)

        # Keep only the content for THIS heading — stop at any subsequent H1/H2 heading
        # so a misbehaving LLM cannot bleed other sections into this one.
        content = self._trim_to_single_section(content.strip())

        logger.success(f"Wrote section '{heading}' ({len(content.split())} words)")

        return {
            'heading': heading,
            'content': content.strip(),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _trim_to_single_section(self, content: str) -> str:
        """
        Ensure the content belongs to only ONE section.

        The LLM is asked to write a single ``## Heading`` block, but it
        sometimes appends additional ``##`` or ``#`` sections.  We keep
        everything up to (but not including) the second top-level (H1/H2)
        heading so that stray sections are stripped before the content is
        used in the combined README.
        """
        lines = content.split('\n')
        result: list[str] = []
        found_main = False

        for line in lines:
            stripped = line.strip()
            # Detect an H1 or H2 heading (but not H3+)
            is_h1 = stripped.startswith('# ')
            is_h2 = stripped.startswith('## ')
            is_top_heading = is_h1 or is_h2

            if not found_main:
                result.append(line)
                if is_top_heading:
                    found_main = True
            else:
                # Stop at the next H1/H2 — that belongs to a different section
                if is_top_heading:
                    break
                result.append(line)

        return '\n'.join(result).strip()
