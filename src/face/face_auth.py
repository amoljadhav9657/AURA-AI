"""
AURA AI Face Authentication Manager
Version: 0.38.0
"""

import cv2

from .face_detector import FaceDetector
from .face_recognizer import FaceRecognizer


class FaceAuthManager:

    def __init__(self):
        self.detector = FaceDetector()
        self.recognizer = FaceRecognizer()

        self.authenticated = False
        self.user = None
        self.status = "locked"

    def is_available(self):
        return (
            self.detector.is_available()
            and self.recognizer.is_available()
        )

    def enroll(self, user_id="amol"):

        if not self.is_available():
            return {
                "success": False,
                "reason": "Face authentication system is unavailable.",
            }

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            camera.release()

            return {
                "success": False,
                "reason": "Camera is unavailable.",
            }

        print("📷 Look at the camera for enrollment...")

        success = False

        try:
            for _ in range(100):

                ok, frame = camera.read()

                if not ok:
                    continue

                faces = self.detector.detect(frame)

                if len(faces) != 1:
                    continue

                success = self.recognizer.enroll_face(
                    frame,
                    faces[0],
                    user_id,
                )

                if success:
                    break

        finally:
            camera.release()

        return {
            "success": success,
            "user": user_id if success else None,
            "reason": (
                "Face enrolled successfully."
                if success
                else "Unable to enroll face."
            ),
        }

    def authenticate(self):

        self.lock()

        if not self.is_available():
            return self.get_status(
                "Face authentication system is unavailable."
            )

        if not self.recognizer.enrolled:
            return self.get_status(
                "No authorized face is enrolled."
            )

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            camera.release()

            return self.get_status(
                "Camera is unavailable."
            )

        try:
            for _ in range(60):

                ok, frame = camera.read()

                if not ok:
                    continue

                faces = self.detector.detect(frame)

                if len(faces) != 1:
                    continue

                result = self.recognizer.recognize_face(
                    frame,
                    faces[0],
                )

                if result["recognized"]:
                    self.authenticated = True
                    self.user = result["user"]
                    self.status = "authorized"

                    return self.get_status(
                        result["reason"]
                    )

        finally:
            camera.release()

        return self.get_status(
            "Face not recognized."
        )

    def lock(self):

        self.authenticated = False
        self.user = None
        self.status = "locked"

    def is_authenticated(self):
        return self.authenticated

    def get_status(self, reason=None):

        result = {
            "authenticated": self.authenticated,
            "status": self.status,
            "user": self.user,
        }

        if reason:
            result["reason"] = reason

        return result
