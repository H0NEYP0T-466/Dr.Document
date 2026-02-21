"""Manager Agent - Reviews individual README sections and provides actionable feedback"""
import re
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class ManagerAgent(BaseAgent):
    """
    Reviews the quality of a single README section.
    Uses the thinking model for thorough analysis.
    Returns approve / reject with improvement notes on rejection.
    """

    def __init__(self):
        # Use thinking model for complex review decisions
        super().__init__("Manager", settings.model_flash_thinking)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review a single README section.

        Args:
            input_data: {
                'heading': str,
                'section_content': str,
                'codebase_summary': str,
                'repo_name': str,
            }

        Returns:
            {
                'approved': bool,
                'quality_score': int (0-100),
                'feedback': str,
                'improvement_notes': str,   # actionable if rejected
            }
        """
        heading = input_data.get('heading', 'Unknown')
        section_content = input_data.get('section_content', '')
        codebase_summary = input_data.get('codebase_summary', '')
        repo_name = input_data.get('repo_name', 'Unknown Repository')

        logger.workflow_step("Manager Review", f"Reviewing '{heading}' section for {repo_name}")

        prompt = (
            f'You are a senior documentation manager reviewing the "{heading}" section '
            f'of a README for the repository "{repo_name}".\n\n'
            f'CODEBASE CONTEXT\n'
            f'{codebase_summary}\n\n'
            f'SECTION CONTENT TO REVIEW:\n'
            f'{section_content}\n\n'
            f'Review this section and provide:\n'
            f'1. QUALITY SCORE (0-100): How good is this section?\n'
            f'2. APPROVAL DECISION: APPROVE or REJECT\n'
            f'3. FEEDBACK: What is good about this section?\n'
            f'4. IMPROVEMENT NOTES (only if rejecting): Specific, actionable improvements needed. '
            f'Be very precise about what is missing, wrong, or needs to change.\n\n'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior engineering manager reviewing documentation quality. "
                    "Provide thorough, constructive reviews with actionable feedback."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        review = self._call_llm(messages, max_tokens=1024)

        approved = self._extract_approval(review)
        quality_score = self._extract_quality_score(review)
        improvement_notes = '' if approved else self._extract_improvement_notes(review)

        if approved:
            logger.success(f"Manager APPROVED '{heading}' — Score: {quality_score}/100")
        else:
            logger.warning(f"Manager REJECTED '{heading}' — Score: {quality_score}/100")

        return {
            'approved': approved,
            'quality_score': quality_score,
            'feedback': review,
            'improvement_notes': improvement_notes,
        }

    # ------------------------------------------------------------------
    # Parsing helpers
    # ------------------------------------------------------------------

    def _extract_approval(self, review: str) -> bool:
        """Extract approval decision from review text."""
        upper = review.upper()
        # Use word-boundary matching to avoid "REJECTION" triggering REJECT
        has_reject = bool(re.search(r'\bREJECT\b', upper))
        has_approve = bool(re.search(r'\bAPPROVED?\b', upper))
        # Explicit APPROVE without standalone REJECT
        if has_approve and not has_reject:
            return True
        # Check decision / approval lines
        for line in upper.split('\n'):
            if 'DECISION' in line or 'APPROVAL' in line:
                line_has_reject = bool(re.search(r'\bREJECT\b', line))
                line_has_approve = bool(re.search(r'\bAPPROVED?\b', line))
                if line_has_approve and not line_has_reject:
                    return True
        return False

    def _extract_quality_score(self, review: str) -> int:
        """Extract numeric quality score (0-100) from review text."""
        patterns = [
            r'(\d{1,3})\s*/\s*100',
            r'[Ss]core[:\s]+(\d{1,3})',
            r'(\d{1,3})\s+out of 100',
        ]
        for pattern in patterns:
            match = re.search(pattern, review)
            if match:
                return min(100, max(0, int(match.group(1))))
        return 70 if self._extract_approval(review) else 50

    def _extract_improvement_notes(self, review: str) -> str:
        """Extract actionable improvement notes from a rejected review."""
        lines = review.split('\n')
        in_notes = False
        notes: list = []

        for line in lines:
            upper_line = line.upper()
            if 'IMPROVEMENT' in upper_line or 'MISSING' in upper_line or 'NEEDS' in upper_line:
                in_notes = True
                continue
            if in_notes:
                # Stop at next top-level numbered section
                stripped = line.strip()
                if stripped and stripped[0].isdigit() and '.' in stripped[:5]:
                    break
                if stripped:
                    notes.append(stripped)

        if notes:
            return '\n'.join(notes)
        # Fallback: last 500 chars of review as context
        return review[-500:].strip()
