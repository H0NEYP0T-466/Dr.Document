"""GitHub repository client for Dr. Document"""
import os
import tempfile
import shutil
from typing import List, Dict, Any, Optional
from git import Repo
from pathlib import Path
from backend.config import settings
from backend.logger import logger


class GitHubClient:
    """Handle GitHub repository operations"""
    
    def __init__(self):
        self.temp_dir = None
        logger.info("GitHub client initialized")
    
    def clone_repository(self, repo_url: str) -> str:
        """
        Clone a GitHub repository to a temporary directory
        
        Args:
            repo_url: GitHub repository URL
        
        Returns:
            Path to cloned repository
        """
        try:
            logger.workflow_step("Repository Cloning", f"Cloning {repo_url}")
            
            # Create temporary directory
            self.temp_dir = tempfile.mkdtemp(prefix="dr_document_")
            logger.info(f"Created temporary directory: {self.temp_dir}")
            
            # Clone the repository
            logger.info(f"Starting git clone operation...")
            repo = Repo.clone_from(repo_url, self.temp_dir)
            
            logger.success(f"Successfully cloned repository to {self.temp_dir}")
            logger.info(f"Repository branch: {repo.active_branch}")
            
            return self.temp_dir
            
        except Exception as e:
            logger.error(f"Failed to clone repository: {str(e)}", exc_info=True)
            self.cleanup()
            raise
    
    def get_repository_files(self, repo_path: str) -> List[Dict[str, Any]]:
        """
        Get all relevant code files from repository
        
        Args:
            repo_path: Path to cloned repository
        
        Returns:
            List of file info dictionaries
        """
        try:
            logger.workflow_step("File Discovery", f"Scanning {repo_path}")
            
            files = []
            excluded_dirs = {
                'node_modules', '.git', '__pycache__', 'venv', 'env',
                'dist', 'build', '.next', '.vscode', '.idea', 'coverage',
                'target', 'bin', 'obj', '.pytest_cache', '.mypy_cache'
            }
            
            repo_root = Path(repo_path)
            
            # Walk through directory
            for file_path in repo_root.rglob('*'):
                # Skip if it's not a file
                if not file_path.is_file():
                    continue
                
                # Skip excluded directories
                if any(excluded in file_path.parts for excluded in excluded_dirs):
                    continue
                
                # Check file extension
                if file_path.suffix not in settings.allowed_file_extensions:
                    continue
                
                # Check file size
                try:
                    file_size = file_path.stat().st_size
                    if file_size > settings.max_file_size:
                        logger.warning(f"Skipping large file: {file_path} ({file_size} bytes)")
                        continue
                    
                    if file_size == 0:
                        logger.warning(f"Skipping empty file: {file_path}")
                        continue
                    
                except Exception as e:
                    logger.warning(f"Could not stat file {file_path}: {e}")
                    continue
                
                # Get relative path from repo root
                relative_path = file_path.relative_to(repo_root)
                
                files.append({
                    'path': str(file_path),
                    'relative_path': str(relative_path),
                    'name': file_path.name,
                    'extension': file_path.suffix,
                    'size': file_size
                })
                
                logger.file_process(str(relative_path), 'Discovered')
            
            logger.success(f"Found {len(files)} files to process")
            
            # Sort files by size (process smaller files first)
            files.sort(key=lambda x: x['size'])
            
            return files
            
        except Exception as e:
            logger.error(f"Failed to scan repository files: {str(e)}", exc_info=True)
            raise
    
    def read_file_content(self, file_path: str) -> Optional[str]:
        """
        Read content of a file
        
        Args:
            file_path: Path to file
        
        Returns:
            File content as string or None if failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            logger.file_process(file_path, 'Read')
            return content
            
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {str(e)}")
            return None
    
    def extract_repo_name(self, repo_url: str) -> str:
        """
        Extract repository name from URL
        
        Args:
            repo_url: GitHub repository URL
        
        Returns:
            Repository name
        """
        # Handle various URL formats
        # https://github.com/user/repo
        # https://github.com/user/repo.git
        # git@github.com:user/repo.git
        
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        
        parts = repo_url.rstrip('/').split('/')
        if len(parts) >= 2:
            return f"{parts[-2]}/{parts[-1]}"
        
        return "unknown-repo"
    
    def cleanup(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                logger.info(f"Cleaning up temporary directory: {self.temp_dir}")
                shutil.rmtree(self.temp_dir)
                logger.success("Cleanup completed")
            except Exception as e:
                logger.error(f"Failed to cleanup: {str(e)}")
    
    def __del__(self):
        """Ensure cleanup on deletion"""
        self.cleanup()
