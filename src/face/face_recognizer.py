"""
AURA AI Face Recognizer
Version: 0.36.0
"""


class FaceRecognizer:

    def __init__(self):
        self.authorized_user = None
        self.enrolled = False

    def enroll(self, user_id):
        if not user_id:
            return False

        self.authorized_user = user_id.strip()
        self.enrolled = True

        return True

    def recognize(self, detected_user):
        if not self.enrolled:
            return {
                "recognized": False,
                "user": None,
                "reason": "No face has been enrolled."
            }

        if detected_user == self.authorized_user:
            return {
                "recognized": True,
                "user": self.authorized_user,
                "reason": "Face recognized."
            }

        return {
            "recognized": False,
            "user": None,
            "reason": "Face not recognized."
        }

    def reset(self):
        self.authorized_user = None
        self.enrolled = False

    def get_status(self):
        return {
            "enrolled": self.enrolled,
            "user": self.authorized_user
        }
