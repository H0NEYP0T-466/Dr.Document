"""Community Manager Agent - Reviews community health files (lenient)"""
import re
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class CommunityManagerAgent(BaseAgent):
    """
    Reviews community health files (LICENSE, CONTRIBUTING, CODE_OF_CONDUCT,
    SECURITY, SUPPORT, CODEOWNERS).

    Much less strict than the README manager — these files follow standard
    templates and only need basic sanity checks.  Only rejects on critical
    issues (completely wrong format, missing mandatory sections, wrong license
    type, etc.).
    """

    def __init__(self):
        super().__init__("Community Manager", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review a single community health file.

        Args:
            input_data: {
                'filename': str,
                'content': str,
                'repo_name': str,
                'repo_owner': str,
            }

        Returns:
            {
                'approved': bool,
                'quality_score': int (0-100),
                'feedback': str,
                'improvement_notes': str,
            }
        """
        filename = input_data.get('filename', 'Unknown')
        content = input_data.get('content', '')
        repo_name = input_data.get('repo_name', 'Unknown')
        repo_owner = input_data.get('repo_owner', '')

        logger.workflow_step("Community Manager", f"Reviewing {filename} for {repo_name}")

        prompt = (
            f'You are reviewing the community health file "{filename}" for the repository '
            f'"{repo_name}" (owner: @{repo_owner}).\n\n'
            f'FILE CONTENT:\n{content}\n\n'
            f'Review this file and provide:\n'
            f'1. QUALITY SCORE (0-100)\n'
            f'2. APPROVAL DECISION: APPROVE or REJECT\n'
            f'3. FEEDBACK: What is good about this file?\n'
            f'4. IMPROVEMENT NOTES (only if rejecting): Specific issues that MUST be fixed.\n\n'
            f'IMPORTANT — Be LENIENT. Only REJECT if:\n'
            f'- The file is completely empty or clearly broken/truncated\n'
            f'- For LICENSE: it is not an MIT license\n'
            f'- For CODEOWNERS: @{repo_owner} is not listed as a default owner\n'
            f'- The file is completely off-topic (wrong file type)\n\n'
            f'Minor formatting issues, slightly different wording from templates, '
            f'or missing optional sections should NOT cause rejection. '
            f'A score of 60+ should almost always be APPROVED.'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a lenient open-source community manager reviewing standard "
                    "community health files. Approve unless there are critical issues."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        review = self._call_llm(messages, max_tokens=512, temperature=0.3)

        approved = self._extract_approval(review)
        quality_score = self._extract_quality_score(review)
        improvement_notes = '' if approved else self._extract_improvement_notes(review)

        if approved:
            logger.success(f"Community Manager APPROVED {filename} — Score: {quality_score}/100")
        else:
            logger.warning(f"Community Manager REJECTED {filename} — Score: {quality_score}/100")

        return {
            'approved': approved,
            'quality_score': quality_score,
            'feedback': review,
            'improvement_notes': improvement_notes,
        }

    def _extract_approval(self, review: str) -> bool:
        upper = review.upper()
        has_reject = bool(re.search(r'\bREJECT\b', upper))
        has_approve = bool(re.search(r'\bAPPROVED?\b', upper))
        if has_approve and not has_reject:
            return True
        for line in upper.split('\n'):
            if 'DECISION' in line or 'APPROVAL' in line:
                if bool(re.search(r'\bAPPROVED?\b', line)) and not bool(re.search(r'\bREJECT\b', line)):
                    return True
        return False

    def _extract_quality_score(self, review: str) -> int:
        patterns = [
            r'(\d{1,3})\s*/\s*100',
            r'[Ss]core[:\s]+(\d{1,3})',
            r'(\d{1,3})\s+out of 100',
        ]
        for pattern in patterns:
            match = re.search(pattern, review)
            if match:
                return min(100, max(0, int(match.group(1))))
        return 75 if self._extract_approval(review) else 55

    def _extract_improvement_notes(self, review: str) -> str:
        lines = review.split('\n')
        in_notes = False
        notes: List[str] = []
        for line in lines:
            upper_line = line.upper()
            if 'IMPROVEMENT' in upper_line or 'MISSING' in upper_line or 'NEEDS' in upper_line:
                in_notes = True
                continue
            if in_notes:
                stripped = line.strip()
                if stripped and stripped[0].isdigit() and '.' in stripped[:5]:
                    break
                if stripped:
                    notes.append(stripped)
        if notes:
            return '\n'.join(notes)
        return review[-300:].strip()
