"""Community Final Reviewer Agent - Reviews all community files together (lenient)"""
import re
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class CommunityFinalReviewerAgent(BaseAgent):
    """
    Reviews the complete set of community health files.
    Much less strict than the README final reviewer.
    Only rejects on truly critical issues that affect the usability
    of the repository's community health files.
    """

    def __init__(self):
        super().__init__("Community Final Reviewer", settings.model_flash_lite)

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the full set of community health files.

        Args:
            input_data: {
                'community_files': List[{'filename': str, 'content': str}],
                'repo_name': str,
                'repo_owner': str,
            }

        Returns:
            {
                'approved': bool,
                'score': int (0-100),
                'issues': List[str],
                'improvement_details': str,
                'final_verdict': str,
            }
        """
        community_files: List[Dict] = input_data.get('community_files', [])
        repo_name = input_data.get('repo_name', 'Unknown')
        repo_owner = input_data.get('repo_owner', '')

        logger.workflow_step("Community Final Reviewer", f"Reviewing all community files for {repo_name}")

        if not community_files:
            return self._rejection_result("No community files provided")

        files_summary = '\n\n'.join(
            f'--- {f["filename"]} ---\n{f["content"][:800]}'
            for f in community_files
        )

        expected_files = ['LICENSE', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md',
                          'SECURITY.md', 'SUPPORT.md', 'CODEOWNERS']
        present = [f['filename'] for f in community_files]
        missing = [name for name in expected_files if name not in present]

        prompt = (
            f'You are doing a final review of the community health files for "{repo_name}" '
            f'(owner: @{repo_owner}).\n\n'
            f'FILES PRESENT: {", ".join(present)}\n'
            f'{"MISSING FILES: " + ", ".join(missing) if missing else "All expected files present."}\n\n'
            f'FILE PREVIEWS:\n{files_summary}\n\n'
            f'Review the set and provide:\n'
            f'1. OVERALL SCORE (0-100)\n'
            f'2. ISSUES FOUND: List any critical problems\n'
            f'3. IMPROVEMENT DETAILS (only if rejecting)\n'
            f'4. FINAL VERDICT: APPROVE or REJECT\n\n'
            f'Be LENIENT — only REJECT if:\n'
            f'- LICENSE is not MIT\n'
            f'- CODEOWNERS does not list @{repo_owner}\n'
            f'- More than 2 files are completely empty or totally broken\n\n'
            f'Minor issues, slight deviations from templates, and missing optional content '
            f'should NOT cause rejection. A score of 60+ warrants APPROVE.'
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a lenient open-source community reviewer. "
                    "Approve community health files unless there are truly critical issues."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        review = self._call_llm(messages, max_tokens=1024, temperature=0.3)

        approved = self._extract_approval(review)
        score = self._extract_score(review)
        issues = self._extract_list(review, 'ISSUES')
        improvement_details = '' if approved else self._extract_improvement_details(review)

        if approved:
            logger.success(f"Community Final Reviewer APPROVED — Score: {score}/100")
        else:
            logger.warning(f"Community Final Reviewer REJECTED — Score: {score}/100")

        return {
            'approved': approved,
            'score': score,
            'issues': issues,
            'improvement_details': improvement_details,
            'final_verdict': review,
        }

    def _extract_approval(self, review: str) -> bool:
        upper = review.upper()
        if 'VERDICT' in upper:
            verdict_part = upper.split('VERDICT')[1][:300]
            if bool(re.search(r'\bAPPROVED?\b', verdict_part)) and not bool(re.search(r'\bREJECT\b', verdict_part)):
                return True
            if bool(re.search(r'\bREJECT\b', verdict_part)):
                return False
        has_approve = bool(re.search(r'\bAPPROVED?\b', upper))
        has_reject = bool(re.search(r'\bREJECT\b', upper))
        if has_approve and not has_reject:
            return True
        return False

    def _extract_score(self, review: str) -> int:
        patterns = [
            r'(\d{1,3})\s*/\s*100',
            r'[Ss]core[:\s]+(\d{1,3})',
            r'(\d{1,3})\s+out of 100',
        ]
        for pattern in patterns:
            match = re.search(pattern, review)
            if match:
                return min(100, max(0, int(match.group(1))))
        return 78 if self._extract_approval(review) else 60

    def _extract_list(self, review: str, section_name: str) -> List[str]:
        items: List[str] = []
        lines = review.split('\n')
        in_section = False
        for line in lines:
            if section_name.upper() in line.upper():
                in_section = True
                continue
            if in_section:
                stripped = line.strip()
                if stripped and stripped[0].isdigit() and '.' in stripped[:5]:
                    break
                if stripped and (stripped.startswith('-') or stripped.startswith('•')):
                    item = stripped.lstrip('-• ')
                    if item:
                        items.append(item)
        return items[:10]

    def _extract_improvement_details(self, review: str) -> str:
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
                if stripped and stripped[0].isdigit() and '.' in stripped[:5]:
                    break
                if stripped:
                    details.append(stripped)
        if details:
            return '\n'.join(details)
        return '\n'.join(self._extract_list(review, 'ISSUES'))

    def _rejection_result(self, reason: str) -> Dict[str, Any]:
        return {
            'approved': False,
            'score': 0,
            'issues': [reason],
            'improvement_details': f'Critical issue: {reason}',
            'final_verdict': f'REJECTED: {reason}',
        }
