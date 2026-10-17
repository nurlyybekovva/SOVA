import logging
from concurrent.futures import ThreadPoolExecutor
from backend.app import jobs
from backend.app.services import analysis_pipeline

log = logging.getLogger("worker")
executor = ThreadPoolExecutor(max_workers=1)


def _process(job_id: str, video_path: str):
    try:
        result = analysis_pipeline.run(video_path)
        jobs.set_done(job_id, result)
    except Exception as e:
        log.exception("Job %s failed", job_id)
        jobs.set_failed(job_id, str(e))


def submit(job_id: str, video_path: str):
    executor.submit(_process, job_id, video_path)