"""Software Documentation Manager Agent"""
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class SoftwareDocManagerAgent(BaseAgent):
    """
    Reviews software documentation sections for quality.
    Can request up to 3 restarts per section.
    """

    def __init__(self):
        super().__init__("Software Doc Manager Agent", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review a single section.

        Args:
            input_data: {
                'section_name': str,
                'section_content': str,
                'section_brief': str,
                'codebase_summary': str,
                'restart_count': int,
            }

        Returns:
            {
                'section_name': str,
                'status': 'APPROVED' | 'RESTART' | 'APPROVED_WITH_WARNING',
                'feedback': str,
                'restart_count': int,
            }
        """
        section_name = input_data.get('section_name', '')
        section_content = input_data.get('section_content', '')
        section_brief = input_data.get('section_brief', '')
        codebase_summary = input_data.get('codebase_summary', '')
        restart_count = input_data.get('restart_count', 0)

        if restart_count >= 3:
            logger.warning(f"Max restarts for '{section_name}' — APPROVED_WITH_WARNING")
            return {
                'section_name': section_name,
                'status': 'APPROVED_WITH_WARNING',
                'feedback': 'Maximum restart limit reached.',
                'restart_count': restart_count,
            }

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a technical documentation reviewer. "
                    "Evaluate the section and provide a clear decision."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Section: {section_name}\n\n"
                    f"Brief:\n{section_brief}\n\n"
                    f"Content:\n{section_content}\n\n"
                    f"Evaluate:\n"
                    f"1. Does it follow the writing brief?\n"
                    f"2. Is it clearly written and explanatory?\n"
                    f"3. Does it have sufficient content (>200 words for substantive sections)?\n"
                    f"4. Is it accurate based on the codebase?\n"
                    f"5. Does it avoid fabrication?\n\n"
                    f"Respond:\n"
                    f"STATUS: APPROVED or RESTART\n"
                    f"FEEDBACK: [specific feedback if RESTART, or 'Meets all criteria']"
                ),
            },
        ]

        raw = self._call_llm(messages, max_tokens=400, temperature=0.3)

        status = 'APPROVED'
        feedback = ''
        for line in raw.strip().splitlines():
            if line.upper().startswith('STATUS:'):
                val = line.split(':', 1)[1].strip().upper()
                if 'RESTART' in val:
                    status = 'RESTART'
            elif line.upper().startswith('FEEDBACK:'):
                feedback = line.split(':', 1)[1].strip()

        if not feedback:
            feedback = raw.strip()

        return {
            'section_name': section_name,
            'status': status,
            'feedback': feedback,
            'restart_count': restart_count + (1 if status == 'RESTART' else 0),
        }

    def review_all_sections(
        self,
        sections: List[Dict[str, Any]],
        codebase_summary: str,
    ) -> Dict[str, Any]:
        """Review all sections and produce manager_review.txt content."""
        results = []
        for sec in sections:
            result = self.run({
                'section_name': sec['name'],
                'section_content': sec['content'],
                'section_brief': sec.get('brief', ''),
                'codebase_summary': codebase_summary,
                'restart_count': sec.get('restart_count', 0),
            })
            results.append(result)

        lines = []
        pipeline_ready = True
        for r in results:
            lines.append(f"{r['section_name']}_STATUS: {r['status']}")
            lines.append(f"{r['section_name']}_FEEDBACK: {r['feedback']}")
            lines.append('')
            if r['status'] == 'RESTART':
                pipeline_ready = False

        lines.append(f"PIPELINE_READY: {'true' if pipeline_ready else 'false'}")

        return {
            'review_txt': '\n'.join(lines),
            'pipeline_ready': pipeline_ready,
            'section_results': results,
        }
