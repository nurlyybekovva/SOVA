import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from app import jobs, worker
from app.config import settings
from app.schemas import AnalyzeResponse
from app.security import verify_api_key

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse, dependencies=[Depends(verify_api_key)])
async def analyze(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in settings.allowed_extensions:
        raise HTTPException(400, f"Unsupported file type: {ext or 'none'}")

    job_id = uuid.uuid4().hex[:12]
    path = settings.upload_dir / f"{job_id}{ext}"
    with open(path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    jobs.create_job(job_id)
    worker.submit(job_id, str(path))
    return {"job_id": job_id}