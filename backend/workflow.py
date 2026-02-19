"""Workflow orchestration for multi-agent documentation generation"""
import asyncio
import json
import os
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from backend.agents.code_reader import CodeReaderAgent
from backend.agents.requirements_extractor import RequirementsExtractorAgent
from backend.agents.manager import ManagerAgent
from backend.agents.readme_writer import ReadmeWriterAgent
from backend.agents.final_reviewer import FinalReviewerAgent
from backend.github_client import GitHubClient
from backend.config import settings
from backend.logger import logger


class WorkflowStatus:
    """Workflow status tracking"""
    PENDING = "pending"
    CLONING = "cloning"
    ANALYZING = "analyzing"
    EXTRACTING = "extracting_requirements"
    REVIEWING = "manager_review"
    WRITING = "writing_readme"
    FINAL_REVIEW = "final_review"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentationWorkflow:
    """Orchestrates the multi-agent documentation generation workflow"""
    
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.status = WorkflowStatus.PENDING
        self.progress = 0
        self.result = None
        self.error = None
        self.status_callback: Optional[Callable] = None
        
        # Initialize agents
        self.code_reader = CodeReaderAgent()
        self.requirements_extractor = RequirementsExtractorAgent()
        self.manager = ManagerAgent()
        self.readme_writer = ReadmeWriterAgent()
        self.final_reviewer = FinalReviewerAgent()
        
        # GitHub client
        self.github_client = GitHubClient()
        
        # Storage
        self.storage_dir = os.path.join(settings.storage_path, job_id)
        os.makedirs(self.storage_dir, exist_ok=True)
        
        logger.info(f"Workflow initialized for job {job_id}")
    
    def set_status_callback(self, callback: Callable):
        """Set callback for status updates"""
        self.status_callback = callback
    
    async def _update_status(self, status: str, progress: int, message: str = ""):
        """Update workflow status"""
        self.status = status
        self.progress = progress
        
        logger.workflow_step(f"Status Update", f"{status} - {progress}% - {message}")
        
        if self.status_callback:
            await self.status_callback({
                'job_id': self.job_id,
                'status': status,
                'progress': progress,
                'message': message,
                'timestamp': datetime.now().isoformat()
            })
    
    async def execute(self, repo_url: str) -> Dict[str, Any]:
        """
        Execute the complete documentation workflow
        
        Args:
            repo_url: GitHub repository URL
        
        Returns:
            Result dictionary with README and metadata
        """
        try:
            logger.info(f"🚀 Starting workflow for {repo_url}")
            
            # Step 1: Clone repository
            await self._update_status(WorkflowStatus.CLONING, 10, "Cloning repository...")
            repo_path = self.github_client.clone_repository(repo_url)
            repo_name = self.github_client.extract_repo_name(repo_url)
            
            # Step 2: Get repository files
            await self._update_status(WorkflowStatus.ANALYZING, 20, "Discovering files...")
            files = self.github_client.get_repository_files(repo_path)
            
            if not files:
                raise ValueError("No supported files found in repository")
            
            # Step 3: Analyze code files (Agent 1)
            await self._update_status(WorkflowStatus.ANALYZING, 25, f"Analyzing {len(files)} files...")
            code_analyses = await self._analyze_files(files)
            
            # Save analyses
            self._save_intermediate("code_analyses.json", code_analyses)
            
            # Step 4: Extract requirements (Agent 2)
            await self._update_status(WorkflowStatus.EXTRACTING, 45, "Extracting requirements...")
            requirements = self.requirements_extractor.run({
                'analyses': code_analyses,
                'repo_name': repo_name
            })
            
            # Save requirements
            self._save_intermediate("requirements.json", requirements)
            
            # Step 5: Manager review (Agent 3) with retry logic
            max_retries = 2
            retry_count = 0
            manager_approved = False
            
            while retry_count <= max_retries and not manager_approved:
                await self._update_status(
                    WorkflowStatus.REVIEWING,
                    55 + (retry_count * 5),
                    f"Manager review (attempt {retry_count + 1})..."
                )
                
                manager_review = self.manager.run({
                    'code_analyses': code_analyses,
                    'requirements': requirements,
                    'repo_name': repo_name
                })
                
                self._save_intermediate(f"manager_review_{retry_count}.json", manager_review)
                
                if manager_review['approved']:
                    manager_approved = True
                    logger.success("Manager approved the analysis!")
                else:
                    retry_count += 1
                    if retry_count <= max_retries and manager_review.get('should_retry', False):
                        logger.warning(f"Manager requested improvements. Retry {retry_count}/{max_retries}")
                        # In a more sophisticated system, we would refine the analyses here
                    else:
                        logger.warning("Manager not fully satisfied but proceeding...")
                        break
            
            # Step 6: Generate README (Agent 4)
            await self._update_status(WorkflowStatus.WRITING, 70, "Writing README...")
            readme_result = self.readme_writer.run({
                'repo_name': repo_name,
                'code_analyses': code_analyses,
                'requirements': requirements,
                'manager_feedback': manager_review.get('feedback', '')
            })
            
            readme_content = readme_result['readme_content']
            
            # Save README draft
            self._save_text("readme_draft.md", readme_content)
            
            # Step 7: Final review (Agent 5)
            await self._update_status(WorkflowStatus.FINAL_REVIEW, 85, "Final review...")
            final_review = self.final_reviewer.run({
                'readme_content': readme_content,
                'code_analyses': code_analyses,
                'requirements': requirements,
                'repo_name': repo_name
            })
            
            self._save_intermediate("final_review.json", final_review)
            
            # Step 8: Finalize
            await self._update_status(WorkflowStatus.COMPLETED, 100, "Documentation complete!")
            
            # Save final README
            self._save_text("README.md", readme_content)
            
            # Prepare result
            result = {
                'job_id': self.job_id,
                'repo_name': repo_name,
                'repo_url': repo_url,
                'readme': readme_content,
                'files_analyzed': len(files),
                'manager_review': {
                    'approved': manager_review['approved'],
                    'quality_score': manager_review['quality_score']
                },
                'final_review': {
                    'approved': final_review['approved'],
                    'completeness_score': final_review['completeness_score'],
                    'accuracy_score': final_review['accuracy_score']
                },
                'storage_path': self.storage_dir,
                'timestamp': datetime.now().isoformat()
            }
            
            self.result = result
            logger.success(f"✅ Workflow completed successfully for {repo_name}")
            
            return result
            
        except Exception as e:
            logger.error(f"Workflow failed: {str(e)}", exc_info=True)
            self.status = WorkflowStatus.FAILED
            self.error = str(e)
            await self._update_status(WorkflowStatus.FAILED, self.progress, f"Error: {str(e)}")
            raise
        
        finally:
            # Cleanup
            self.github_client.cleanup()
    
    async def _analyze_files(self, files: List[Dict]) -> List[Dict]:
        """Analyze all code files"""
        analyses = []
        total = len(files)
        
        # Limit files to analyze (for efficiency)
        max_files = 30
        files_to_analyze = files[:max_files]
        
        if len(files) > max_files:
            logger.info(f"Limiting analysis to {max_files} most relevant files out of {total}")
        
        for idx, file_info in enumerate(files_to_analyze):
            try:
                # Update progress
                progress = 25 + int((idx / len(files_to_analyze)) * 20)
                await self._update_status(
                    WorkflowStatus.ANALYZING,
                    progress,
                    f"Analyzing {file_info['relative_path']}..."
                )
                
                # Read file content
                content = self.github_client.read_file_content(file_info['path'])
                
                if content:
                    # Analyze with Agent 1
                    analysis = self.code_reader.run({
                        'file_path': file_info['relative_path'],
                        'file_content': content,
                        'language': file_info['extension']
                    })
                    
                    analyses.append(analysis)
                
            except Exception as e:
                logger.error(f"Failed to analyze {file_info['relative_path']}: {str(e)}")
                continue
        
        logger.success(f"Completed analysis of {len(analyses)} files")
        return analyses
    
    def _save_intermediate(self, filename: str, data: Any):
        """Save intermediate results as JSON"""
        try:
            filepath = os.path.join(self.storage_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.file_process(filename, 'Saved intermediate result')
        except Exception as e:
            logger.error(f"Failed to save {filename}: {str(e)}")
    
    def _save_text(self, filename: str, content: str):
        """Save text content"""
        try:
            filepath = os.path.join(self.storage_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.file_process(filename, 'Saved text file')
        except Exception as e:
            logger.error(f"Failed to save {filename}: {str(e)}")
