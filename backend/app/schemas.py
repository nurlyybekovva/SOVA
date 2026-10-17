from typing import Literal
from pydantic import BaseModel


# ---- Output for the jury (strict) ----
class EvidenceFrame(BaseModel):
    timestamp_sec: float
    image_base64: str


class Violation(BaseModel):
    type: str
    timecode_sec: float
    description: str
    evidence_frames: list[EvidenceFrame]


class AnalyzeResponse(BaseModel):
    job_id: str


class JobResult(BaseModel):
    job_id: str
    status: Literal["processing", "done", "failed"]
    verdict: Literal["violation", "no_violation"] | None = None
    violations: list[Violation] | None = None


# ---- Internal ML contract  ----
class MLEvent(BaseModel):
    type: str
    start_sec: float
    end_sec: float
    description: str
    evidence_timestamp: float


class MLOutput(BaseModel):
    events: list[MLEvent]