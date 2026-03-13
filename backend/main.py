"""FastAPI backend for Dr. Document"""
import asyncio
import uuid
import shutil
import mimetypes
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from backend.workflow import DocumentationWorkflow, WorkflowStatus
from backend.logger import logger
from backend.config import settings
import os

# Create storage directory
os.makedirs(settings.storage_path, exist_ok=True)

# Jobs directory for multi-mode output
JOBS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jobs')
os.makedirs(JOBS_DIR, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title="Dr. Document API",
    description="AI-Powered GitHub Documentation Generator",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for workflow instances
workflows: Dict[str, DocumentationWorkflow] = {}

# WebSocket connections
connections: Dict[str, WebSocket] = {}

# Multi-mode jobs storage: job_id -> job state dict
multi_mode_jobs: Dict[str, Dict[str, Any]] = {}


class ProcessRepoRequest(BaseModel):
    """Request model for repository processing"""
    repo_url: HttpUrl


class ProcessRepoResponse(BaseModel):
    """Response model for repository processing"""
    job_id: str
    status: str
    message: str


class StatusResponse(BaseModel):
    """Response model for status check"""
    job_id: str
    status: str
    progress: int
    message: str


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.success("🚀 Dr. Document API started successfully!")
    logger.info(f"Storage path: {settings.storage_path}")
    logger.info(f"LongCat API configured: {bool(settings.longcat_api_key)}")

    # Check for pdflatex system binary availability
    pdflatex_path = shutil.which('pdflatex')
    if pdflatex_path:
        logger.info(f"pdflatex found: {pdflatex_path}")
    else:
        logger.warning(
            "pdflatex binary not found — PDF output will be unavailable.\n"
            "  'pip install pdflatex' only installs a Python wrapper and does NOT provide the binary.\n"
            "  Install the system package instead:\n"
            "    Ubuntu/Debian : sudo apt-get install texlive-latex-base\n"
            "    Fedora/RHEL   : sudo dnf install texlive-latex\n"
            "    macOS         : brew install basictex  (or install MacTeX)\n"
            "    Windows       : install MiKTeX from https://miktex.org"
        )

    # Schedule periodic job directory cleanup every 6 hours
    async def _periodic_cleanup():
        while True:
            await asyncio.sleep(6 * 3600)
            try:
                _cleanup_old_jobs()
            except Exception as e:
                logger.error(f"Job cleanup failed: {e}")

    asyncio.create_task(_periodic_cleanup())


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Dr. Document API",
        "version": "1.0.0",
        "status": "operational",
        "description": "AI-Powered GitHub Documentation Generator"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_jobs": len(workflows),
        "storage_path": settings.storage_path
    }


@app.post("/api/process-repo", response_model=ProcessRepoResponse)
async def process_repository(request: ProcessRepoRequest):
    """
    Start processing a GitHub repository
    
    Args:
        request: Repository URL to process
    
    Returns:
        Job ID and status
    """
    try:
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        logger.info(f"📥 New repository request: {request.repo_url}")
        logger.info(f"Assigned job ID: {job_id}")
        
        # Create workflow instance
        workflow = DocumentationWorkflow(job_id)
        workflows[job_id] = workflow
        
        # Set status callback for WebSocket updates
        async def status_callback(status_data):
            if job_id in connections:
                try:
                    await connections[job_id].send_json(status_data)
                except Exception as e:
                    logger.error(f"Failed to send WebSocket update: {e}")
        
        workflow.set_status_callback(status_callback)
        
        # Start workflow in background
        asyncio.create_task(workflow.execute(str(request.repo_url)))
        
        return ProcessRepoResponse(
            job_id=job_id,
            status=WorkflowStatus.PENDING,
            message="Repository processing started"
        )
        
    except Exception as e:
        logger.error(f"Failed to start repository processing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str):
    """
    Get status of a job
    
    Args:
        job_id: Job identifier
    
    Returns:
        Current status and progress
    """
    if job_id not in workflows:
        raise HTTPException(status_code=404, detail="Job not found")
    
    workflow = workflows[job_id]
    
    return StatusResponse(
        job_id=job_id,
        status=workflow.status,
        progress=workflow.progress,
        message=workflow.error or "Processing"
    )


@app.get("/api/result/{job_id}")
async def get_result(job_id: str):
    """
    Get result of a completed job
    
    Args:
        job_id: Job identifier
    
    Returns:
        Complete result including README
    """
    if job_id not in workflows:
        raise HTTPException(status_code=404, detail="Job not found")
    
    workflow = workflows[job_id]
    
    if workflow.status == WorkflowStatus.FAILED:
        raise HTTPException(status_code=500, detail=workflow.error)
    
    if workflow.status != WorkflowStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    if not workflow.result:
        raise HTTPException(status_code=500, detail="Result not available")
    
    return workflow.result


@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    """
    WebSocket endpoint for real-time updates
    
    Args:
        websocket: WebSocket connection
        job_id: Job identifier
    """
    await websocket.accept()
    connections[job_id] = websocket
    
    logger.info(f"WebSocket connected for job {job_id}")
    
    try:
        # Send initial status if workflow exists
        if job_id in workflows:
            workflow = workflows[job_id]
            await websocket.send_json({
                'job_id': job_id,
                'status': workflow.status,
                'progress': workflow.progress,
                'message': 'Connected'
            })
        
        # Keep connection alive
        while True:
            # Wait for messages (ping/pong)
            data = await websocket.receive_text()
            
            # Echo back for keep-alive
            if data == "ping":
                await websocket.send_text("pong")
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for job {job_id}")
        if job_id in connections:
            del connections[job_id]
    except Exception as e:
        logger.error(f"WebSocket error for job {job_id}: {str(e)}")
        if job_id in connections:
            del connections[job_id]


@app.delete("/api/job/{job_id}")
async def delete_job(job_id: str):
    """
    Delete a job and its data
    
    Args:
        job_id: Job identifier
    
    Returns:
        Deletion confirmation
    """
    if job_id not in workflows:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        # Remove from memory
        del workflows[job_id]
        
        # Remove storage directory
        storage_dir = os.path.join(settings.storage_path, job_id)
        if os.path.exists(storage_dir):
            import shutil
            shutil.rmtree(storage_dir)
        
        logger.info(f"Deleted job {job_id}")
        
        return {"message": "Job deleted successfully"}
        
    except Exception as e:
        logger.error(f"Failed to delete job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Multi-mode generate endpoints
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    """Request body for POST /api/generate"""
    repo_url: HttpUrl
    modes: List[str]  # e.g. ["software_doc", "srs"]
    options: Optional[Dict[str, Any]] = {}


class GenerateResponse(BaseModel):
    """Response for POST /api/generate"""
    job_id: str
    modes_started: List[str]


async def _run_multi_mode_job(
    job_id: str,
    repo_url: str,
    modes: List[str],
    codebase_summary: str,
    repo_name: str,
):
    """Background task: run requested mode workflows in parallel."""
    from backend.workflows.software_doc_workflow import SoftwareDocWorkflow
    from backend.workflows.srs_workflow import SRSWorkflow

    job = multi_mode_jobs[job_id]
    loop = asyncio.get_running_loop()
    job_dir = os.path.join(JOBS_DIR, job_id)

    async def emit(event: Dict[str, Any]):
        event['job_id'] = job_id
        if job_id in connections:
            try:
                await connections[job_id].send_json(event)
            except Exception:
                pass

    # Build workflow instances per mode
    workflow_map = {
        'software_doc': lambda: SoftwareDocWorkflow(
            job_dir=job_dir,
            codebase_summary=codebase_summary,
            repo_name=repo_name,
            repo_url=repo_url,
            status_callback=emit,
        ),
        'srs': lambda: SRSWorkflow(
            job_dir=job_dir,
            codebase_summary=codebase_summary,
            repo_name=repo_name,
            repo_url=repo_url,
            status_callback=emit,
        ),
    }

    async def run_mode(mode: str):
        job['modes'][mode]['status'] = 'processing'
        await emit({'type': 'mode_started', 'mode': mode})
        try:
            factory = workflow_map.get(mode)
            if factory is None:
                job['modes'][mode]['status'] = 'failed'
                job['modes'][mode]['error'] = f'Unknown mode: {mode}'
                return
            wf = factory()
            result = await wf.execute(loop)
            job['modes'][mode]['status'] = 'completed'
            # Store relative file paths (filename only) for download endpoint
            files = {}
            for fmt, path in result.get('files', {}).items():
                if path and os.path.exists(path):
                    fname = os.path.basename(path)
                    files[fmt] = f'/download/{job_id}/{fname}'
            job['modes'][mode]['files'] = files
            await emit({'type': 'mode_completed', 'mode': mode, 'files': list(files.keys())})
        except Exception as e:
            logger.error(f"Mode {mode} failed for job {job_id}: {e}", exc_info=True)
            job['modes'][mode]['status'] = 'failed'
            job['modes'][mode]['error'] = str(e)
            await emit({'type': 'mode_failed', 'mode': mode, 'error': str(e)})

    # Run all modes in parallel
    await asyncio.gather(*[run_mode(m) for m in modes])

    # Mark overall job done
    job['status'] = 'completed'
    job['completed_at'] = datetime.utcnow().isoformat()
    await emit({'type': 'job_completed', 'job_id': job_id})


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    """
    Start a multi-mode documentation generation job.

    Modes: software_doc, srs
    All selected modes run in parallel after shared codebase analysis.
    """
    from backend.github_client import GitHubClient
    from backend.agents.codebase_summarizer import CodebaseSummarizerAgent
    from backend.config import settings as cfg

    valid_modes = {'software_doc', 'srs'}
    modes = [m for m in request.modes if m in valid_modes]
    if not modes:
        raise HTTPException(status_code=400, detail="No valid modes specified")

    job_id = str(uuid.uuid4())
    job_dir = os.path.join(JOBS_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    repo_url = str(request.repo_url)

    job: Dict[str, Any] = {
        'job_id': job_id,
        'repo_url': repo_url,
        'modes': {m: {'status': 'pending', 'files': {}} for m in modes},
        'status': 'processing',
        'created_at': datetime.utcnow().isoformat(),
    }
    multi_mode_jobs[job_id] = job

    # Clone repo and summarize codebase (shared step)
    try:
        github_client = GitHubClient()
        loop = asyncio.get_running_loop()

        repo_path = await loop.run_in_executor(
            None, github_client.clone_repository, repo_url
        )
        repo_name = github_client.extract_repo_name(repo_url)

        files = await loop.run_in_executor(
            None, github_client.get_repository_files, repo_path
        )
        max_files = cfg.max_files_to_analyze
        if len(files) > max_files:
            files = files[:max_files]

        # Run codebase summarizer
        summarizer = CodebaseSummarizerAgent()
        lines: List[str] = []
        for file_info in files:
            try:
                content = await loop.run_in_executor(
                    None, github_client.read_file_content, file_info['path']
                )
                if content:
                    result = await loop.run_in_executor(
                        None, summarizer.run,
                        {'file_path': file_info['relative_path'], 'file_content': content},
                    )
                    lines.append(f"{result['file_path']} = {result['summary']}")
            except Exception as exc:
                logger.warning(f"Skipped {file_info.get('relative_path', '?')}: {exc}")

        codebase_summary = '\n'.join(lines)

        # Save codebase summary to job dir
        with open(os.path.join(job_dir, 'codebase_summary.txt'), 'w', encoding='utf-8') as f:
            f.write(codebase_summary)

        github_client.cleanup()

    except Exception as e:
        logger.error(f"Failed to initialize job {job_id}: {e}", exc_info=True)
        job['status'] = 'failed'
        raise HTTPException(status_code=500, detail=f"Failed to analyze repository: {e}")

    # Launch mode pipelines in background
    asyncio.create_task(
        _run_multi_mode_job(job_id, repo_url, modes, codebase_summary, repo_name)
    )

    return GenerateResponse(job_id=job_id, modes_started=modes)


@app.get("/api/results/{job_id}")
async def get_results(job_id: str):
    """
    Get results for a multi-mode generation job.

    Returns status and file download URLs for all modes.
    """
    if job_id not in multi_mode_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = multi_mode_jobs[job_id]
    return {
        'job_id': job_id,
        'status': job['status'],
        'modes': job['modes'],
    }


@app.get("/download/{job_id}/{filename}")
async def download_file(job_id: str, filename: str):
    """
    Stream download of a generated file.

    Returns the file with appropriate Content-Disposition headers.
    """
    # Prevent path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    file_path = os.path.join(JOBS_DIR, job_id, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Detect MIME type
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=mime_type,
        headers={'Content-Disposition': f'attachment; filename="{filename}"'},
    )


def _cleanup_old_jobs():
    """Remove job directories older than 24 hours."""
    cutoff = datetime.utcnow() - timedelta(hours=24)
    expired = [
        jid for jid, j in multi_mode_jobs.items()
        if datetime.fromisoformat(j.get('created_at', datetime.utcnow().isoformat())) < cutoff
    ]
    for jid in expired:
        job_dir = os.path.join(JOBS_DIR, jid)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir, ignore_errors=True)
        del multi_mode_jobs[jid]
        logger.info(f"Cleaned up expired job {jid}")


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Dr. Document API server...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8004   ,
        reload=True,
        log_level="info"
    )
