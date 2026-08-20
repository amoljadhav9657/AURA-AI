"""
=========================================
AURA AI - Face Authentication Foundation
Version: 0.35.0
=========================================
"""

from enum import Enum


class AuthStatus(Enum):
    AUTHORIZED = "authorized"
    DENIED = "denied"
    LOCKED = "locked"


class FaceAuthManager:

    def __init__(self):
        self.status = AuthStatus.LOCKED
        self.authorized_user = None

    def authenticate(self, user_id=None):
        """
        Foundation/mock authentication.

        Actual camera + face recognition will be
        connected later without changing this interface.
        """

        if not user_id:
            self.status = AuthStatus.DENIED
            self.authorized_user = None
            return {
                "authenticated": False,
                "status": self.status.value,
                "user": None,
            }

        self.status = AuthStatus.AUTHORIZED
        self.authorized_user = user_id

        return {
            "authenticated": True,
            "status": self.status.value,
            "user": user_id,
        }

    def lock(self):
        self.status = AuthStatus.LOCKED
        self.authorized_user = None

    def is_authenticated(self):
        return self.status == AuthStatus.AUTHORIZED

    def get_status(self):
        return {
            "authenticated": self.is_authenticated(),
            "status": self.status.value,
            "user": self.authorized_user,
        }
