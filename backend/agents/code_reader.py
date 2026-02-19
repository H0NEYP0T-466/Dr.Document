"""Agent 1: Code Reader - Analyzes code files"""
from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.config import settings
from backend.logger import logger


class CodeReaderAgent(BaseAgent):
    """Analyzes code structure, functions, classes, and dependencies"""
    
    def __init__(self):
        super().__init__("Code Reader", settings.model_flash_lite)
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a code file
        
        Args:
            input_data: {
                'file_path': str,
                'file_content': str,
                'language': str (optional)
            }
        
        Returns:
            {
                'file_path': str,
                'analysis': str,
                'functions': list,
                'classes': list,
                'dependencies': list,
                'summary': str
            }
        """
        file_path = input_data.get('file_path', 'unknown')
        file_content = input_data.get('file_content', '')
        language = input_data.get('language', 'unknown')
        
        logger.file_process(file_path, 'Analyzing')
        
        if not file_content.strip():
            logger.warning(f"Empty file content for {file_path}")
            return {
                'file_path': file_path,
                'analysis': 'Empty file',
                'functions': [],
                'classes': [],
                'dependencies': [],
                'summary': 'No content to analyze'
            }
        
        # Prepare prompt for LLM
        prompt = f"""Analyze the following {language} code file and provide a comprehensive analysis.

File: {file_path}

Code:
```
{file_content[:3000]}  # Limit to first 3000 chars
```

Please analyze and provide:
1. Main purpose and functionality
2. List of functions/methods with brief descriptions
3. List of classes/interfaces with brief descriptions
4. External dependencies and imports
5. Key algorithms or patterns used
6. Overall code quality observations

Format your response as a structured analysis."""
        
        messages = [
            {
                "role": "system",
                "content": "You are a code analysis expert. Analyze code thoroughly and provide structured insights."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call LLM
        analysis_result = self._call_llm(messages, max_tokens=2000)
        
        # Parse the analysis (simplified extraction)
        result = {
            'file_path': file_path,
            'analysis': analysis_result,
            'functions': self._extract_functions(analysis_result),
            'classes': self._extract_classes(analysis_result),
            'dependencies': self._extract_dependencies(analysis_result),
            'summary': self._extract_summary(analysis_result)
        }
        
        logger.success(f"Completed analysis for {file_path}")
        
        return result
    
    def _extract_functions(self, analysis: str) -> list:
        """Extract function names from analysis"""
        # Simple extraction - look for function mentions
        functions = []
        lines = analysis.split('\n')
        for line in lines:
            if 'function' in line.lower() or 'method' in line.lower():
                # Simple extraction logic
                parts = line.split(':')
                if len(parts) >= 2:
                    functions.append(parts[0].strip())
        return functions[:20]  # Limit to 20 functions
    
    def _extract_classes(self, analysis: str) -> list:
        """Extract class names from analysis"""
        classes = []
        lines = analysis.split('\n')
        for line in lines:
            if 'class' in line.lower():
                parts = line.split(':')
                if len(parts) >= 2:
                    classes.append(parts[0].strip())
        return classes[:20]  # Limit to 20 classes
    
    def _extract_dependencies(self, analysis: str) -> list:
        """Extract dependencies from analysis"""
        dependencies = []
        lines = analysis.split('\n')
        for line in lines:
            if 'import' in line.lower() or 'dependency' in line.lower() or 'require' in line.lower():
                parts = line.split(':')
                if len(parts) >= 2:
                    dependencies.append(parts[1].strip())
        return dependencies[:30]  # Limit to 30 dependencies
    
    def _extract_summary(self, analysis: str) -> str:
        """Extract summary from analysis"""
        lines = analysis.split('\n')
        # Take first meaningful paragraph as summary
        summary_lines = []
        for line in lines[:10]:
            if line.strip() and not line.startswith('#'):
                summary_lines.append(line.strip())
                if len(summary_lines) >= 3:
                    break
        return ' '.join(summary_lines) if summary_lines else analysis[:200]
