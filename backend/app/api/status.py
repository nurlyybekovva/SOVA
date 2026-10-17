from fastapi import APIRouter, Depends, HTTPException
from app import jobs
from  app.security import verify_api_key

router = APIRouter()


@router.get("/jobs/{job_id}", dependencies=[Depends(verify_api_key)])
def get_job(job_id: str):
    job = jobs.get_job(job_id)
    if job is None:
        raise HTTPException(404, "Job not found")
    if job["status"] == "done":
        return {"job_id": job_id, "status": "done", **job["result"]}
    return {"job_id": job_id, "status": job["status"]}   # processing / failed