"""Final Reviewer Agent - Reviews the complete combined README and approves or requests a full redo"""
import re
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class FinalReviewerAgent(BaseAgent):
    """
    Reviews the assembled README as a whole.
    Uses the thinking model for thorough validation.
    On rejection, provides improvement details so the section-writing cycle
    can be restarted (up to 3 full cycles total).
    """

    def __init__(self):
        super().__init__("Final Reviewer", settings.model_flash_thinking)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the full combined README.

        Args:
            input_data: {
                'readme_content': str,
                'codebase_summary': str,
                'repo_name': str,
            }

        Returns:
            {
                'approved': bool,
                'completeness_score': int (0-100),
                'accuracy_score': int (0-100),
                'issues': List[str],
                'improvement_details': str,   # actionable notes for next cycle
                'final_verdict': str,
            }
        """
        readme_content = input_data.get('readme_content', '')
        codebase_summary = input_data.get('codebase_summary', '')
        repo_name = input_data.get('repo_name', 'Unknown')

        logger.workflow_step("Final Review", f"Validating README for {repo_name}")

        if not readme_content.strip():
            logger.error("Empty README content provided for final review")
            return self._rejection_result("README content is empty")

        prompt = (
            f'You are conducting a final quality review of a generated README for "{repo_name}".\n\n'
            f'CODEBASE CONTEXT (file summaries — first 3000 chars):\n'
            f'{codebase_summary}\n\n'
            f'GENERATED README:\n'
            f'{readme_content}\n\n'
            f'Please validate the README thoroughly:\n\n'
            f'1. COMPLETENESS CHECK (0-100):\n'
            f'   - Are all essential sections present?\n'
            f'   - Is technical information comprehensive?\n'
            f'   - Are usage examples provided?\n'
            f'   - Is setup/installation covered?\n\n'
            f'2. ACCURACY CHECK (0-100):\n'
            f'   - Does content match the codebase?\n'
            f'   - Are technical details correct?\n'
            f'   - Are features accurately described?\n\n'
            f'3. ISSUES FOUND:\n'
            f'   - List any problems, inaccuracies, or missing critical information.\n\n'
            f'4. IMPROVEMENT DETAILS (only if rejecting):\n'
            f'   - Very specific, actionable notes for the next documentation cycle.\n'
            f'   - Focus only on critical missing/incorrect content.\n\n'
            f'5. FINAL VERDICT:\n'
            f'   - APPROVE or REJECT with clear reasoning.\n'
            f'   - Only REJECT if there are critical issues that significantly '
            f'undermine the usefulness of the README.'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior documentation reviewer with expertise in technical writing "
                    "and software documentation standards. Be thorough but avoid unnecessary restarts."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        review = self._call_llm(messages, max_tokens=2048)

        approved = self._extract_approval(review)
        completeness = self._extract_score(review, 'COMPLETENESS')
        accuracy = self._extract_score(review, 'ACCURACY')
        issues = self._extract_list(review, 'ISSUES')
        improvement_details = '' if approved else self._extract_improvement_details(review)

        overall = (completeness + accuracy) / 2

        if approved:
            logger.success(f"Final Review APPROVED — Overall: {overall:.1f}/100")
        else:
            logger.warning(f"Final Review REJECTED — Overall: {overall:.1f}/100")

        return {
            'approved': approved,
            'completeness_score': completeness,
            'accuracy_score': accuracy,
            'issues': issues,
            'improvement_details': improvement_details,
            'final_verdict': review,
        }

    # ------------------------------------------------------------------
    # Parsing helpers
    # ------------------------------------------------------------------

    def _extract_approval(self, review: str) -> bool:
        """Extract final approval decision."""
        upper = review.upper()

        # Check VERDICT section first
        if 'VERDICT' in upper:
            verdict_part = upper.split('VERDICT')[1][:300]
            verdict_reject = bool(re.search(r'\bREJECT\b', verdict_part))
            verdict_approve = bool(re.search(r'\bAPPROVED?\b', verdict_part))
            if verdict_approve and not verdict_reject:
                return True
            if verdict_reject:
                return False

        has_approval = bool(re.search(r'\bAPPROVED?\b', upper))
        has_rejection = bool(re.search(r'\bREJECT\b', upper))

        if has_approval and not has_rejection:
            return True
        return False

    def _extract_score(self, review: str, category: str) -> int:
        """Extract numeric score for a category section."""
        lines = review.split('\n')
        for i, line in enumerate(lines):
            if category.upper() in line.upper():
                search_text = '\n'.join(lines[i: i + 5])
                patterns = [
                    r'(\d{1,3})\s*/\s*100',
                    r'[Ss]core[:\s]+(\d{1,3})',
                    r'(\d{1,3})\s+out of 100',
                    r':\s*(\d{1,3})',
                ]
                for pattern in patterns:
                    match = re.search(pattern, search_text)
                    if match:
                        return min(100, max(0, int(match.group(1))))
        return 75 if self._extract_approval(review) else 60

    def _extract_list(self, review: str, section_name: str) -> List[str]:
        """Extract bullet-point items from a named section."""
        items: List[str] = []
        lines = review.split('\n')
        in_section = False

        for line in lines:
            if section_name.upper() in line.upper():
                in_section = True
                continue
            if in_section:
                stripped = line.strip()
                # Stop at next numbered section
                if stripped and stripped[0].isdigit() and '.' in stripped[:5]:
                    break
                if stripped and (
                    stripped.startswith('-')
                    or stripped.startswith('•')
                    or (stripped[0].isdigit() and '.' in stripped[:3])
                ):
                    item = stripped.lstrip('-•0123456789. ')
                    if item:
                        items.append(item)

        return items[:15]

    def _extract_improvement_details(self, review: str) -> str:
        """Extract improvement details for the next documentation cycle."""
        lines = review.split('\n')
        in_section = False
        details: List[str] = []

        for line in lines:
            upper_line = line.upper()
            if 'IMPROVEMENT' in upper_line or ('DETAIL' in upper_line and in_section):
                in_section = True
                continue
            if in_section:
                stripped = line.strip()
                # Stop at next numbered section
                if stripped and stripped[0].isdigit() and '.' in stripped[:5]:
                    break
                if stripped:
                    details.append(stripped)

        if details:
            return '\n'.join(details)
        # Fallback: include the full issues list
        return '\n'.join(self._extract_list(review, 'ISSUES'))

    def _rejection_result(self, reason: str) -> Dict[str, Any]:
        """Return a structured rejection result."""
        return {
            'approved': False,
            'completeness_score': 0,
            'accuracy_score': 0,
            'issues': [reason],
            'improvement_details': f'Critical issue: {reason}',
            'final_verdict': f'REJECTED: {reason}',
        }
