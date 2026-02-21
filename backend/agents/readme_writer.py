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
2. BADGES SECTION - Include GitHub badges using shields.io right after the title. Use this exact format (replace OWNER/REPO with the actual repo name):

<p>
  <img src="https://img.shields.io/github/license/OWNER/REPO?style=for-the-badge&color=blue" alt="GitHub License">
  <img src="https://img.shields.io/github/stars/OWNER/REPO?style=for-the-badge&color=yellow" alt="GitHub Stars">
  <img src="https://img.shields.io/github/forks/OWNER/REPO?style=for-the-badge&color=green" alt="GitHub Forks">
  <img src="https://img.shields.io/github/issues/OWNER/REPO?style=for-the-badge&color=red" alt="GitHub Issues">
  <img src="https://img.shields.io/github/issues-pr/OWNER/REPO?style=for-the-badge&color=orange" alt="GitHub Pull Requests">
</p>

<p>
  <img src="https://img.shields.io/github/last-commit/OWNER/REPO?style=for-the-badge&color=purple" alt="Last Commit">
  <img src="https://img.shields.io/github/commit-activity/m/OWNER/REPO?style=for-the-badge&color=brightgreen" alt="Commit Activity">
  <img src="https://img.shields.io/github/languages/top/OWNER/REPO?style=for-the-badge&color=blueviolet" alt="Top Language">
  <img src="https://img.shields.io/github/languages/count/OWNER/REPO?style=for-the-badge&color=ff69b4" alt="Language Count">
</p>

<p>
  <img src="https://img.shields.io/github/repo-size/OWNER/REPO?style=for-the-badge&color=important" alt="Repo Size">
  <img src="https://img.shields.io/github/contributors/OWNER/REPO?style=for-the-badge&color=success" alt="Contributors">
  <img src="https://img.shields.io/github/watchers/OWNER/REPO?style=for-the-badge&color=informational" alt="Watchers">
  <img src="https://img.shields.io/github/downloads/OWNER/REPO/total?style=for-the-badge&color=blue" alt="Downloads">
</p>

<p>
  <img src="https://img.shields.io/badge/code%20style-standard-brightgreen?style=for-the-badge" alt="Code Style">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/maintained-yes-green.svg?style=for-the-badge" alt="Maintained">
  <img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red.svg?style=for-the-badge" alt="Open Source">
</p>

3. DESCRIPTION - Clear, engaging overview
4. FEATURES - Key capabilities and highlights
5. TECH STACK BADGES - Use shields.io badges for all technologies. Format each technology as a badge:
   <img src="https://img.shields.io/badge/TECHNOLOGY_NAME-COLOR?style=for-the-badge&logo=LOGO_NAME&logoColor=white">
   Use appropriate colors and logos from simpleicons.org (e.g., Python=3776AB, React=61DAFB, FastAPI=009688, Docker=2496ED, PostgreSQL=4169E1, TypeScript=3178C6, JavaScript=F7DF1E, Node.js=339933, etc.)
   Group them in <p> tags.  
6. ARCHITECTURE - System design and patterns
7. INSTALLATION/Usage - Setup instructions
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
- ALWAYS include the shields.io badges section right after the title
- ALWAYS render the tech stack as badges instead of plain text
- Never mention the file name or any other irrelevant things only releated to the README content

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
        readme_content = self._call_llm(messages, max_tokens=8192)
        
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
