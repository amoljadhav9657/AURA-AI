"""
AURA AI Face Authentication Manager
Version: 0.36.0
"""

from .face_detector import FaceDetector
from .face_recognizer import FaceRecognizer


class FaceAuthManager:

    def __init__(self):
        self.detector = FaceDetector()
        self.recognizer = FaceRecognizer()

        self.authenticated = False
        self.user = None
        self.status = "locked"

    def enroll(self, user_id):
        if not user_id:
            return False

        return self.recognizer.enroll(user_id)

    def authenticate(self, detected_user=None):
        if not self.recognizer.enrolled:
            self.authenticated = False
            self.user = None
            self.status = "denied"

            return self.get_status()

        result = self.recognizer.recognize(detected_user)

        if result["recognized"]:
            self.authenticated = True
            self.user = result["user"]
            self.status = "authorized"
        else:
            self.authenticated = False
            self.user = None
            self.status = "denied"

        return self.get_status()

    def lock(self):
        self.authenticated = False
        self.user = None
        self.status = "locked"

    def is_authenticated(self):
        return self.authenticated

    def get_status(self):
        return {
            "authenticated": self.authenticated,
            "status": self.status,
            "user": self.user,
        }
