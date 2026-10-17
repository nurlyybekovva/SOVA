import logging
import time
from app.config import settings
from app.schemas import MLOutput
from app.services import compliance_engine, evidence_generator

log = logging.getLogger("pipeline")
_analyzer = None


def get_analyzer():
    """Load the model ONCE and reuse it for every job."""
    global _analyzer
    if _analyzer is None:
        if settings.use_stub:
            from app.ml.stub_analyzer import StubAnalyzer
            _analyzer = StubAnalyzer()
        else:
            from app.ml.qwen_analyzer import QwenAnalyzer  # written by participant #4
            _analyzer = QwenAnalyzer()
    return _analyzer


def run(video_path: str) -> dict:
    t0 = time.time()
    raw = get_analyzer().analyze(video_path)
    ml = MLOutput(**raw)                      # validates the internal contract
    t1 = time.time()

    violations = compliance_engine.evaluate([e.model_dump() for e in ml.events])
    violations = evidence_generator.attach_evidence(video_path, violations)
    t2 = time.time()

    log.info("ML %.1fs | rules+evidence %.1fs | total %.1fs", t1 - t0, t2 - t1, t2 - t0)
    return {
        "verdict": "violation" if violations else "no_violation",
        "violations": violations,
    }