from backend.app.ml.base import BaseVideoAnalyzer
from backend.app.services.video_processor import get_video_info


class StubAnalyzer(BaseVideoAnalyzer):
    def analyze(self, video_path: str) -> dict:
        duration = get_video_info(video_path)["duration"]
        mid = round(duration / 2, 2)
        return {"events": [{
            "type": "cash_handling_event",
            "start_sec": max(0.0, mid - 2),
            "end_sec": min(duration, mid + 2),
            "description": "STUB: observed cash handling action",
            "evidence_timestamp": mid,
        }]}