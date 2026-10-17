class BaseVideoAnalyzer:
    def analyze(self, video_path: str) -> dict:
        """Must return {"events": [{type, start_sec, end_sec, description, evidence_timestamp}]}"""
        raise NotImplementedError