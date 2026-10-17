import base64
import cv2
import numpy as np


def get_video_info(path: str) -> dict:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("Cannot open video file")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return {"fps": fps, "frame_count": int(n_frames), "duration": n_frames / fps}


def make_segments(duration: float, length: float, overlap: float) -> list[tuple[float, float]]:
    """Overlapping windows in ORIGINAL video seconds, e.g. 0-10, 8-18, 16-26..."""
    segments, start, step = [], 0.0, length - overlap
    while start < duration:
        end = min(start + length, duration)
        segments.append((round(start, 2), round(end, 2)))
        if end >= duration:
            break
        start += step
    return segments


def sample_timestamps(start: float, end: float, n: int) -> list[float]:
    return [round(float(t), 2) for t in np.linspace(start, max(start, end - 0.05), n)]


def extract_frame(path: str, t_sec: float):
    """Return a BGR frame at t_sec of the original video (or None)."""
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(t_sec * fps)))
    ok, frame = cap.read()
    cap.release()
    return frame if ok else None


def extract_frames(path: str, timestamps: list[float]) -> list[tuple[float, np.ndarray]]:
    """Open the file once and grab many frames (faster than extract_frame in a loop)."""
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    out = []
    for t in timestamps:
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(t * fps)))
        ok, frame = cap.read()
        if ok:
            out.append((t, frame))
    cap.release()
    return out


def frame_to_base64(frame, max_side: int = 960, quality: int = 80) -> str:
    h, w = frame.shape[:2]
    scale = max_side / max(h, w)
    if scale < 1:
        frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise ValueError("JPEG encoding failed")
    return base64.b64encode(buf).decode("ascii")