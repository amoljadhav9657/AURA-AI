"""
AURA AI Face Detector
Version: 0.37.1

OpenCV YuNet / FaceDetectorYN based detector.
"""

from pathlib import Path

try:
    import cv2
except ImportError:
    cv2 = None


class FaceDetector:

    def __init__(self, model_path=None):
        self.available = cv2 is not None
        self.detector = None

        if not self.available:
            return

        if model_path is None:
            model_path = (
                Path(__file__).resolve().parent
                / "models"
                / "face_detection_yunet_2023mar.onnx"
            )

        self.model_path = Path(model_path)

        if not self.model_path.exists():
            return

        self.detector = cv2.FaceDetectorYN.create(
            str(self.model_path),
            "",
            (320, 320),
            0.6,
            0.3,
            5000,
        )

    def is_available(self):
        return (
            self.available
            and self.detector is not None
        )

    def detect(self, frame):
        if not self.available:
            raise RuntimeError(
                "OpenCV is not installed."
            )

        if self.detector is None:
            raise RuntimeError(
                "YuNet face detection model is unavailable."
            )

        if frame is None:
            return []

        height, width = frame.shape[:2]

        self.detector.setInputSize((width, height))

        _, faces = self.detector.detect(frame)

        if faces is None:
            return []

        return list(faces)
