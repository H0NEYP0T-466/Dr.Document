"""Agent 2: Requirements Extractor - Extracts functional and non-functional requirements"""
from typing import Dict, Any, List
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class RequirementsExtractorAgent(BaseAgent):
    """Extracts functional and non-functional requirements from code analysis"""
    
    def __init__(self):
        super().__init__("Requirements Extractor", settings.model_flash_lite)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract requirements from code analyses
        
        Args:
            input_data: {
                'analyses': List[Dict] - List of code analyses from Agent 1
                'repo_name': str
            }
        
        Returns:
            {
                'functional_requirements': List[str],
                'non_functional_requirements': List[str],
                'technical_stack': List[str],
                'architecture_patterns': List[str],
                'full_specification': str
            }
        """
        analyses = input_data.get('analyses', [])
        repo_name = input_data.get('repo_name', 'Unknown Repository')
        
        logger.workflow_step("Requirements Extraction", f"Processing {len(analyses)} analyses")
        
        if not analyses:
            logger.warning("No analyses provided for requirements extraction")
            return self._empty_requirements()
        
        # Combine all analyses
        combined_analysis = self._combine_analyses(analyses)
        
        # Prepare prompt for LLM
        prompt = f"""Based on the following code analyses for repository '{repo_name}', extract comprehensive requirements.

Combined Code Analysis:
{combined_analysis}

Please extract and categorize:

1. FUNCTIONAL REQUIREMENTS:
   - What features does the system provide?
   - What can users do with this system?
   - What are the main use cases?

2. NON-FUNCTIONAL REQUIREMENTS:
   - Performance requirements
   - Security considerations
   - Scalability aspects
   - Reliability and availability
   - Maintainability concerns

3. TECHNICAL STACK:
   - Programming languages
   - Frameworks and libraries
   - Tools and technologies

4. ARCHITECTURE PATTERNS:
   - Design patterns used
   - Architectural style
   - Component organization

Format each section clearly with bullet points."""
        
        messages = [
            {
                "role": "system",
                "content": "You are a requirements engineering expert. Extract clear, actionable requirements from code analyses."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call LLM
        requirements_text = self._call_llm(messages, max_tokens=8192)
        
        # Parse the requirements
        result = {
            'functional_requirements': self._extract_section(requirements_text, 'FUNCTIONAL'),
            'non_functional_requirements': self._extract_section(requirements_text, 'NON-FUNCTIONAL'),
            'technical_stack': self._extract_section(requirements_text, 'TECHNICAL STACK'),
            'architecture_patterns': self._extract_section(requirements_text, 'ARCHITECTURE'),
            'full_specification': requirements_text
        }
        
        logger.success(f"Extracted requirements for {repo_name}")
        logger.info(f"Found {len(result['functional_requirements'])} functional requirements")
        logger.info(f"Found {len(result['non_functional_requirements'])} non-functional requirements")
        
        return result
    
    def _combine_analyses(self, analyses: List[Dict]) -> str:
        """Combine multiple code analyses into one text"""
        combined = []
        for analysis in analyses:
            file_path = analysis.get('file_path', 'unknown')
            summary = analysis.get('summary', '')
            analysis_text = analysis.get('analysis', '')
            
            combined.append(f"\nFile: {file_path}")
            combined.append(f"Summary: {summary}")
            combined.append(f"Analysis: {analysis_text[:500]}")  # Limit each analysis
        
        return '\n'.join(combined)
    
    def _extract_section(self, text: str, section_name: str) -> List[str]:
        """Extract items from a specific section"""
        items = []
        in_section = False
        lines = text.split('\n')
        
        for line in lines:
            if section_name.upper() in line.upper():
                in_section = True
                continue
            
            if in_section:
                # Stop at next major section
                if line.strip() and line.strip()[0].isdigit() and '.' in line[:3]:
                    break
                
                # Extract bullet points or numbered items
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line.startswith('*') or
                           (line[0].isdigit() and '.' in line[:3])):
                    # Remove bullet/number prefix
                    item = line.lstrip('-•*0123456789. ')
                    if item:
                        items.append(item)
        
        return items[:15]  # Limit to 15 items per section
    
    def _empty_requirements(self) -> Dict[str, Any]:
        """Return empty requirements structure"""
        return {
            'functional_requirements': [],
            'non_functional_requirements': [],
            'technical_stack': [],
            'architecture_patterns': [],
            'full_specification': 'No requirements could be extracted'
        }
