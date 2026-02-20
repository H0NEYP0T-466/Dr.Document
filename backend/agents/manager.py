"""Agent 3: Manager/Overseer - Quality review and approval"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class ManagerAgent(BaseAgent):
    """Reviews quality of analyses and requirements, provides feedback"""
    
    def __init__(self):
        # Use thinking model for complex decisions
        super().__init__("Manager/Overseer", settings.model_flash_thinking)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review code analyses and requirements for quality
        
        Args:
            input_data: {
                'code_analyses': List[Dict],
                'requirements': Dict,
                'repo_name': str
            }
        
        Returns:
            {
                'approved': bool,
                'quality_score': int (0-100),
                'feedback': str,
                'improvement_suggestions': List[str],
                'should_retry': bool
            }
        """
        code_analyses = input_data.get('code_analyses', [])
        requirements = input_data.get('requirements', {})
        repo_name = input_data.get('repo_name', 'Unknown Repository')
        
        logger.workflow_step("Manager Review", f"Reviewing quality for {repo_name}")
        
        # Prepare review prompt
        analyses_summary = self._summarize_analyses(code_analyses)
        requirements_summary = self._summarize_requirements(requirements)
        
        prompt = f"""You are a senior engineering manager reviewing documentation preparation work.

Repository: {repo_name}

CODE ANALYSES SUMMARY:
{analyses_summary}

REQUIREMENTS EXTRACTED:
{requirements_summary}

Please review this work and provide:

1. QUALITY ASSESSMENT (0-100 score):
   - Completeness of analysis
   - Accuracy of requirements extraction
   - Coverage of all important aspects
   - Clarity and organization

2. APPROVAL DECISION:
   - Should this proceed to README generation? (YES/NO)
   - If NO, what improvements are needed?

3. SPECIFIC FEEDBACK:
   - What was done well?
   - What needs improvement?
   - What is missing?

4. IMPROVEMENT SUGGESTIONS:
   - Concrete steps to improve the documentation

Be constructive and specific in your feedback."""
        
        messages = [
            {
                "role": "system",
                "content": "You are a senior engineering manager with expertise in documentation and code quality. Provide thorough, constructive reviews."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call LLM for review
        review_result = self._call_llm(messages, max_tokens=8192)
        
        # Parse the review
        result = {
            'approved': self._extract_approval(review_result),
            'quality_score': self._extract_quality_score(review_result),
            'feedback': review_result,
            'improvement_suggestions': self._extract_suggestions(review_result),
            'should_retry': self._should_retry(review_result)
        }
        
        if result['approved']:
            logger.success(f"Manager APPROVED - Quality Score: {result['quality_score']}/100")
        else:
            logger.warning(f"Manager REJECTED - Quality Score: {result['quality_score']}/100")
            logger.info(f"Retry recommended: {result['should_retry']}")
        
        return result
    
    def _summarize_analyses(self, analyses: list) -> str:
        """Create summary of code analyses"""
        if not analyses:
            return "No code analyses provided"
        
        summary_parts = []
        summary_parts.append(f"Total files analyzed: {len(analyses)}")
        
        total_functions = sum(len(a.get('functions', [])) for a in analyses)
        total_classes = sum(len(a.get('classes', [])) for a in analyses)
        
        summary_parts.append(f"Total functions found: {total_functions}")
        summary_parts.append(f"Total classes found: {total_classes}")
        
        # Add sample file summaries
        summary_parts.append("\nSample analyses:")
        for analysis in analyses[:3]:  # First 3 files
            file_path = analysis.get('file_path', 'unknown')
            summary = analysis.get('summary', 'No summary')
            summary_parts.append(f"- {file_path}: {summary[:100]}")
        
        return '\n'.join(summary_parts)
    
    def _summarize_requirements(self, requirements: Dict) -> str:
        """Create summary of requirements"""
        if not requirements:
            return "No requirements provided"
        
        functional = requirements.get('functional_requirements', [])
        non_functional = requirements.get('non_functional_requirements', [])
        tech_stack = requirements.get('technical_stack', [])
        
        summary = []
        summary.append(f"Functional Requirements: {len(functional)}")
        if functional:
            summary.append("  Examples:")
            for req in functional[:3]:
                summary.append(f"  - {req}")
        
        summary.append(f"\nNon-Functional Requirements: {len(non_functional)}")
        if non_functional:
            summary.append("  Examples:")
            for req in non_functional[:3]:
                summary.append(f"  - {req}")
        
        summary.append(f"\nTechnical Stack: {', '.join(tech_stack[:10])}")
        
        return '\n'.join(summary)
    
    def _extract_approval(self, review: str) -> bool:
        """Extract approval decision from review"""
        review_upper = review.upper()
        # Look for explicit YES in approval decision
        if 'YES' in review_upper and 'APPROVAL' in review_upper:
            return True
        if 'APPROVED' in review_upper:
            return True
        if 'PROCEED' in review_upper and 'YES' in review_upper:
            return True
        # Default to rejected if not clearly approved
        return False
    
    def _extract_quality_score(self, review: str) -> int:
        """Extract quality score from review"""
        import re
        # Look for patterns like "75/100" or "Score: 75" or "75 out of 100"
        patterns = [
            r'(\d{1,3})/100',
            r'[Ss]core[:\s]+(\d{1,3})',
            r'(\d{1,3})\s+out of 100'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, review)
            if match:
                score = int(match.group(1))
                return min(100, max(0, score))  # Ensure 0-100 range
        
        # Default score based on approval
        return 70 if self._extract_approval(review) else 50
    
    def _extract_suggestions(self, review: str) -> list:
        """Extract improvement suggestions from review"""
        suggestions = []
        lines = review.split('\n')
        in_suggestions = False
        
        for line in lines:
            if 'IMPROVEMENT' in line.upper() or 'SUGGESTION' in line.upper():
                in_suggestions = True
                continue
            
            if in_suggestions:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or 
                           (line[0].isdigit() and '.' in line[:3])):
                    suggestion = line.lstrip('-•0123456789. ')
                    if suggestion:
                        suggestions.append(suggestion)
        
        return suggestions[:10]  # Limit to 10 suggestions
    
    def _should_retry(self, review: str) -> bool:
        """Determine if retry is recommended"""
        review_upper = review.upper()
        # If not approved and quality seems improvable
        if not self._extract_approval(review):
            score = self._extract_quality_score(review)
            # Retry if score is between 40-70 (improvable range)
            return 40 <= score <= 70
        return False
