from backend.app.services.video_processor import extract_frames, frame_to_base64, get_video_info


def attach_evidence(video_path: str, violations: list[dict]) -> list[dict]:
    duration = get_video_info(video_path)["duration"]
    result = []
    for v in violations:
        t = v["timecode_sec"]
        # frame at the event plus one just before and after
        times = sorted({max(0.0, t - 1.0), t, min(duration, t + 1.0)})
        frames = extract_frames(video_path, times)
        result.append({
            **v,
            "evidence_frames": [
                {"timestamp_sec": ts, "image_base64": frame_to_base64(fr)}
                for ts, fr in frames
            ],
        })
    return result