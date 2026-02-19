"""FastAPI backend for Dr. Document"""
import asyncio
import uuid
from typing import Dict, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from backend.workflow import DocumentationWorkflow, WorkflowStatus
from backend.logger import logger
from backend.config import settings
import os

# Create storage directory
os.makedirs(settings.storage_path, exist_ok=True)

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


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Dr. Document API server...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
