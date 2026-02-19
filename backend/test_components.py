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
        
        from backend.agents.code_reader import CodeReaderAgent
        print("✓ Code reader agent imported")
        
        from backend.agents.requirements_extractor import RequirementsExtractorAgent
        print("✓ Requirements extractor agent imported")
        
        from backend.agents.manager import ManagerAgent
        print("✓ Manager agent imported")
        
        from backend.agents.readme_writer import ReadmeWriterAgent
        print("✓ README writer agent imported")
        
        from backend.agents.final_reviewer import FinalReviewerAgent
        print("✓ Final reviewer agent imported")
        
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
        assert settings.model_flash_chat == "LongCat-Flash-Chat"
        assert settings.max_files_to_analyze == 30
        
        print(f"✓ Config loaded:")
        print(f"  - Flash Lite model: {settings.model_flash_lite}")
        print(f"  - Flash Chat model: {settings.model_flash_chat}")
        print(f"  - Max files to analyze: {settings.max_files_to_analyze}")
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Dr. Document - Backend Component Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Logger", test_logger()))
    results.append(("Config", test_config()))
    
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
