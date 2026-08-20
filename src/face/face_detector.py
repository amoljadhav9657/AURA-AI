"""
AURA AI Face Detector
Version: 0.36.0
"""

try:
    import cv2
except ImportError:
    cv2 = None


class FaceDetector:

    def __init__(self):
        self.available = cv2 is not None

    def is_available(self):
        return self.available

    def detect(self, frame):
        if not self.available:
            raise RuntimeError(
                "OpenCV is not installed. Face detection is unavailable."
            )

        # Actual detector will be connected in the next step.
        return []
