"""Agent 5: Final Reviewer - Validates README completeness and accuracy"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class FinalReviewerAgent(BaseAgent):
    """Validates the generated README against original analyses"""
    
    def __init__(self):
        # Use thinking model for thorough validation
        super().__init__("Final Reviewer", settings.model_flash_thinking)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate generated README
        
        Args:
            input_data: {
                'readme_content': str,
                'code_analyses': List[Dict],
                'requirements': Dict,
                'repo_name': str
            }
        
        Returns:
            {
                'approved': bool,
                'completeness_score': int (0-100),
                'accuracy_score': int (0-100),
                'issues': List[str],
                'recommendations': List[str],
                'final_verdict': str
            }
        """
        readme_content = input_data.get('readme_content', '')
        code_analyses = input_data.get('code_analyses', [])
        requirements = input_data.get('requirements', {})
        repo_name = input_data.get('repo_name', 'Unknown')
        
        logger.workflow_step("Final Review", f"Validating README for {repo_name}")
        
        if not readme_content.strip():
            logger.error("Empty README content provided for review")
            return self._rejection_result("README content is empty")
        
        # Prepare validation prompt
        validation_context = self._prepare_validation_context(
            readme_content, code_analyses, requirements, repo_name
        )
        
        prompt = f"""You are conducting a final quality review of generated documentation.

{validation_context}

Please validate the README thoroughly:

1. COMPLETENESS CHECK (0-100):
   - Are all essential sections present?
   - Is technical information comprehensive?
   - Are usage examples provided?
   - Is setup/installation covered?

2. ACCURACY CHECK (0-100):
   - Does content match the code analyses?
   - Are technical details correct?
   - Are features accurately described?
   - Are dependencies correctly listed?

3. QUALITY ASSESSMENT:
   - Is the writing clear and professional?
   - Is formatting proper (Markdown)?
   - Are there any grammatical issues?
   - Is the tone appropriate?

4. ISSUES FOUND:
   - List any problems or inaccuracies
   - Note missing critical information
   - Identify misleading content

5. RECOMMENDATIONS:
   - Suggestions for improvement
   - Additional sections to add
   - Content to expand

6. FINAL VERDICT:
   - APPROVE or REJECT with clear reasoning

Be thorough and constructive."""
        
        messages = [
            {
                "role": "system",
                "content": "You are a senior documentation reviewer with expertise in technical writing and software documentation standards."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call LLM for final review
        review_result = self._call_llm(messages, max_tokens=3000)
        
        # Parse the review
        result = {
            'approved': self._extract_approval(review_result),
            'completeness_score': self._extract_score(review_result, 'COMPLETENESS'),
            'accuracy_score': self._extract_score(review_result, 'ACCURACY'),
            'issues': self._extract_list(review_result, 'ISSUES'),
            'recommendations': self._extract_list(review_result, 'RECOMMENDATIONS'),
            'final_verdict': review_result
        }
        
        overall_score = (result['completeness_score'] + result['accuracy_score']) / 2
        
        if result['approved']:
            logger.success(f"Final Review APPROVED - Overall Score: {overall_score:.1f}/100")
        else:
            logger.warning(f"Final Review REJECTED - Overall Score: {overall_score:.1f}/100")
        
        logger.info(f"Completeness: {result['completeness_score']}/100")
        logger.info(f"Accuracy: {result['accuracy_score']}/100")
        logger.info(f"Issues found: {len(result['issues'])}")
        
        return result
    
    def _prepare_validation_context(
        self, readme: str, analyses: list, requirements: Dict, repo_name: str
    ) -> str:
        """Prepare context for validation"""
        context = []
        
        context.append(f"Repository: {repo_name}")
        context.append("")
        
        context.append("GENERATED README (first 2000 chars):")
        context.append(readme[:2000])
        context.append("")
        
        context.append("ORIGINAL ANALYSES SUMMARY:")
        context.append(f"- Total files analyzed: {len(analyses)}")
        
        if analyses:
            total_functions = sum(len(a.get('functions', [])) for a in analyses)
            total_classes = sum(len(a.get('classes', [])) for a in analyses)
            context.append(f"- Total functions: {total_functions}")
            context.append(f"- Total classes: {total_classes}")
        
        context.append("")
        
        context.append("REQUIREMENTS SUMMARY:")
        functional = requirements.get('functional_requirements', [])
        non_functional = requirements.get('non_functional_requirements', [])
        tech_stack = requirements.get('technical_stack', [])
        
        context.append(f"- Functional requirements: {len(functional)}")
        context.append(f"- Non-functional requirements: {len(non_functional)}")
        context.append(f"- Technologies: {', '.join(tech_stack[:10])}")
        context.append("")
        
        return '\n'.join(context)
    
    def _extract_approval(self, review: str) -> bool:
        """Extract approval decision"""
        review_upper = review.upper()
        
        # Look for explicit approval
        if 'APPROVE' in review_upper and 'VERDICT' in review_upper:
            # Check if it's NOT rejected
            if 'REJECT' not in review_upper.split('VERDICT')[1][:200]:
                return True
        
        # Look for approval keywords
        approval_keywords = ['APPROVED', 'ACCEPT', 'APPROVE']
        rejection_keywords = ['REJECT', 'DECLINED', 'DENIED']
        
        has_approval = any(keyword in review_upper for keyword in approval_keywords)
        has_rejection = any(keyword in review_upper for keyword in rejection_keywords)
        
        # If both present, look at context
        if has_approval and has_rejection:
            # Check which appears in verdict section
            if 'VERDICT' in review_upper:
                verdict_section = review_upper.split('VERDICT')[1][:300]
                return any(keyword in verdict_section for keyword in approval_keywords)
        
        # Default based on presence
        return has_approval and not has_rejection
    
    def _extract_score(self, review: str, category: str) -> int:
        """Extract score for a specific category"""
        import re
        
        # Find the category section
        lines = review.split('\n')
        for i, line in enumerate(lines):
            if category.upper() in line.upper():
                # Look in this line and next few lines for a score
                search_text = '\n'.join(lines[i:i+5])
                
                patterns = [
                    r'(\d{1,3})/100',
                    r'[Ss]core[:\s]+(\d{1,3})',
                    r'(\d{1,3})\s+out of 100',
                    r':\s+(\d{1,3})'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, search_text)
                    if match:
                        score = int(match.group(1))
                        return min(100, max(0, score))
        
        # Default score
        return 75 if self._extract_approval(review) else 60
    
    def _extract_list(self, review: str, section_name: str) -> list:
        """Extract items from a section"""
        items = []
        lines = review.split('\n')
        in_section = False
        
        for line in lines:
            if section_name.upper() in line.upper():
                in_section = True
                continue
            
            if in_section:
                # Stop at next numbered section
                if line.strip() and line.strip()[0].isdigit() and '.' in line[:5]:
                    break
                
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or 
                           (line[0].isdigit() and '.' in line[:3])):
                    item = line.lstrip('-•0123456789. ')
                    if item:
                        items.append(item)
        
        return items[:15]  # Limit to 15 items
    
    def _rejection_result(self, reason: str) -> Dict[str, Any]:
        """Return rejection result"""
        return {
            'approved': False,
            'completeness_score': 0,
            'accuracy_score': 0,
            'issues': [reason],
            'recommendations': ['Generate valid README content'],
            'final_verdict': f'REJECTED: {reason}'
        }
