"""Agent 4: README Writer - Generates comprehensive README.md"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class ReadmeWriterAgent(BaseAgent):
    """Generates comprehensive README documentation"""
    
    def __init__(self):
        # Use chat model for content generation
        super().__init__("README Writer", settings.model_flash_chat)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate README from approved analyses
        
        Args:
            input_data: {
                'repo_name': str,
                'code_analyses': List[Dict],
                'requirements': Dict,
                'manager_feedback': str (optional)
            }
        
        Returns:
            {
                'readme_content': str,
                'sections': List[str],
                'word_count': int
            }
        """
        repo_name = input_data.get('repo_name', 'Project')
        code_analyses = input_data.get('code_analyses', [])
        requirements = input_data.get('requirements', {})
        manager_feedback = input_data.get('manager_feedback', '')
        
        logger.workflow_step("README Generation", f"Writing documentation for {repo_name}")
        
        # Prepare comprehensive context
        context = self._prepare_context(repo_name, code_analyses, requirements, manager_feedback)
        
        # Prepare prompt for README generation
        prompt = f"""Generate a comprehensive, professional README.md file for a GitHub repository.

{context}

Create a complete README with the following sections:

1. PROJECT TITLE with emoji
2. DESCRIPTION - Clear, engaging overview
3. FEATURES - Key capabilities and highlights
4. TECHNICAL STACK - Technologies used
5. ARCHITECTURE - System design and patterns
6. INSTALLATION - Setup instructions
7. USAGE - How to use the project
8. API DOCUMENTATION (if applicable)
9. CONFIGURATION - Environment variables and settings
10. CONTRIBUTING - Guidelines for contributors
11. LICENSE - License information
12. ACKNOWLEDGMENTS - Credits and thanks

Requirements:
- Use proper Markdown formatting
- Include emojis where appropriate (🚀 📚 ⚙️ etc.)
- Be professional and engaging
- Include code examples where relevant
- Make it comprehensive and detailed
- Use tables, lists, and formatting for readability

Generate a README that will make developers excited to use this project!"""
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert technical writer specializing in GitHub documentation. Create clear, comprehensive, and engaging README files."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call LLM to generate README
        readme_content = self._call_llm(messages, max_tokens=4000)
        
        # Process the generated README
        result = {
            'readme_content': readme_content,
            'sections': self._extract_sections(readme_content),
            'word_count': len(readme_content.split())
        }
        
        logger.success(f"Generated README with {result['word_count']} words")
        logger.info(f"Sections included: {', '.join(result['sections'])}")
        
        return result
    
    def _prepare_context(self, repo_name: str, analyses: list, requirements: Dict, feedback: str) -> str:
        """Prepare context for README generation"""
        context_parts = []
        
        context_parts.append(f"Repository Name: {repo_name}")
        context_parts.append("")
        
        # Add technical stack
        tech_stack = requirements.get('technical_stack', [])
        if tech_stack:
            context_parts.append("Technical Stack:")
            for tech in tech_stack[:15]:
                context_parts.append(f"- {tech}")
            context_parts.append("")
        
        # Add functional requirements
        functional = requirements.get('functional_requirements', [])
        if functional:
            context_parts.append("Key Features/Capabilities:")
            for req in functional[:10]:
                context_parts.append(f"- {req}")
            context_parts.append("")
        
        # Add architecture patterns
        patterns = requirements.get('architecture_patterns', [])
        if patterns:
            context_parts.append("Architecture Patterns:")
            for pattern in patterns[:5]:
                context_parts.append(f"- {pattern}")
            context_parts.append("")
        
        # Add code structure overview
        if analyses:
            context_parts.append(f"Project Structure ({len(analyses)} files analyzed):")
            file_types = {}
            for analysis in analyses:
                file_path = analysis.get('file_path', '')
                ext = file_path.split('.')[-1] if '.' in file_path else 'other'
                file_types[ext] = file_types.get(ext, 0) + 1
            
            for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]:
                context_parts.append(f"- .{ext}: {count} files")
            context_parts.append("")
        
        # Add manager feedback if available
        if feedback:
            context_parts.append("Manager's Guidance:")
            context_parts.append(feedback[:500])
            context_parts.append("")
        
        return '\n'.join(context_parts)
    
    def _extract_sections(self, readme: str) -> list:
        """Extract section headers from README"""
        sections = []
        lines = readme.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for markdown headers
            if line.startswith('#'):
                # Remove # symbols and clean up
                section = line.lstrip('#').strip()
                # Remove emojis for clean section names
                section = ''.join(c for c in section if c.isalnum() or c.isspace() or c in ['-', '_'])
                if section:
                    sections.append(section.strip())
        
        return sections
