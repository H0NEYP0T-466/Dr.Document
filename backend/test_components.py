"""
Quick test to verify backend components can be imported and initialized
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that all major components can be imported"""
    print("Testing imports...")
    
    try:
        from backend.config import settings
        print("✓ Config imported")
        
        from backend.logger import logger
        print("✓ Logger imported")
        
        from backend.github_client import GitHubClient
        print("✓ GitHub client imported")
        
        from backend.agents.base_agent import BaseAgent
        print("✓ Base agent imported")
        
        from backend.agents.codebase_summarizer import CodebaseSummarizerAgent
        print("✓ Codebase Summarizer agent imported")
        
        from backend.agents.headings_selector import HeadingsSelectorAgent
        print("✓ Headings Selector agent imported")
        
        from backend.agents.section_writer import SectionWriterAgent
        print("✓ Section Writer agent imported")
        
        from backend.agents.manager import ManagerAgent
        print("✓ Manager agent imported")
        
        from backend.agents.final_reviewer import FinalReviewerAgent
        print("✓ Final Reviewer agent imported")
        
        from backend.workflow import DocumentationWorkflow
        print("✓ Workflow imported")
        
        from backend.main import app
        print("✓ FastAPI app imported")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_logger():
    """Test that logger works correctly"""
    print("\nTesting logger...")
    
    try:
        from backend.logger import logger
        
        logger.info("Test info message", emoji='START')
        logger.success("Test success message")
        logger.warning("Test warning message")
        
        print("✓ Logger working correctly")
        return True
    except Exception as e:
        print(f"✗ Logger test failed: {e}")
        return False


def test_config():
    """Test that configuration is loaded"""
    print("\nTesting configuration...")
    
    try:
        from backend.config import settings
        
        assert settings.model_flash_lite == "LongCat-Flash-Lite"
        assert settings.model_flash_thinking == "LongCat-Flash-Thinking"
        assert settings.max_files_to_analyze == 90
        
        print(f"✓ Config loaded:")
        print(f"  - Flash Lite model: {settings.model_flash_lite}")
        print(f"  - Flash Thinking model: {settings.model_flash_thinking}")
        print(f"  - Max files to analyze: {settings.max_files_to_analyze}")
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


def test_agent_init():
    """Test that agents can be instantiated (without API calls)"""
    print("\nTesting agent instantiation (mock API key)...")
    
    try:
        # Temporarily set a dummy API key so OpenAI client doesn't raise
        import os
        os.environ.setdefault("LONGCAT_API_KEY", "test-key")
        
        from backend.agents.codebase_summarizer import CodebaseSummarizerAgent
        a1 = CodebaseSummarizerAgent()
        print(f"✓ CodebaseSummarizerAgent: {a1.agent_name}, model={a1.model}")
        
        from backend.agents.headings_selector import HeadingsSelectorAgent
        a2 = HeadingsSelectorAgent()
        print(f"✓ HeadingsSelectorAgent: {a2.agent_name}, model={a2.model}")
        
        from backend.agents.section_writer import SectionWriterAgent
        a3 = SectionWriterAgent("Features")
        print(f"✓ SectionWriterAgent: {a3.agent_name}, model={a3.model}")
        
        from backend.agents.manager import ManagerAgent
        a4 = ManagerAgent()
        print(f"✓ ManagerAgent: {a4.agent_name}, model={a4.model}")
        
        from backend.agents.final_reviewer import FinalReviewerAgent
        a5 = FinalReviewerAgent()
        print(f"✓ FinalReviewerAgent: {a5.agent_name}, model={a5.model}")
        
        return True
    except Exception as e:
        print(f"✗ Agent instantiation failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Dr. Document - Backend Component Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Logger", test_logger()))
    results.append(("Config", test_config()))
    results.append(("Agent Init", test_agent_init()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed!")
        sys.exit(1)

