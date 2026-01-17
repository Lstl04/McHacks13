from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId

from ..models import Job, JobCreate, JobUpdate, MessageResponse
from ..database import get_database

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=Job, status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate):
    """Create a new job"""
    db = get_database()
    
    # Validate IDs
    if not ObjectId.is_valid(job.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    if not ObjectId.is_valid(job.client_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client ID format"
        )
    
    # Insert job
    job_dict = job.model_dump(exclude_unset=True)
    result = db.jobs.insert_one(job_dict)
    
    # Return created job
    created_job = db.jobs.find_one({"_id": result.inserted_id})
    return created_job

@router.get("/", response_model=List[Job])
async def get_jobs(
    user_id: str = None,
    client_id: str = None,
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100
):
    """Get all jobs with optional filters"""
    db = get_database()
    
    query = {}
    if user_id:
        query["user_id"] = user_id
    if client_id:
        query["client_id"] = client_id
    if status_filter:
        query["status"] = status_filter
    
    jobs = list(db.jobs.find(query).skip(skip).limit(limit))
    return jobs

@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    """Get a specific job by ID"""
    db = get_database()
    
    if not ObjectId.is_valid(job_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format"
        )
    
    job = db.jobs.find_one({"_id": ObjectId(job_id)})
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job

@router.put("/{job_id}", response_model=Job)
async def update_job(job_id: str, job_update: JobUpdate):
    """Update a job"""
    db = get_database()
    
    if not ObjectId.is_valid(job_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format"
        )
    
    update_data = job_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    result = db.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    updated_job = db.jobs.find_one({"_id": ObjectId(job_id)})
    return updated_job

@router.delete("/{job_id}", response_model=MessageResponse)
async def delete_job(job_id: str):
    """Delete a job"""
    db = get_database()
    
    if not ObjectId.is_valid(job_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format"
        )
    
    result = db.jobs.delete_one({"_id": ObjectId(job_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return {"message": f"Job {job_id} deleted successfully"}
