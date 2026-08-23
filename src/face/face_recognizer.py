"""
AURA AI Face Recognizer
Version: 0.40.0

SFace-based face recognition using OpenCV.
"""

from pathlib import Path
import cv2
import numpy as np


class FaceRecognizer:

    def __init__(self):

        self.authorized_user = None
        self.enrolled = False
        self.available = False

        base_path = Path(__file__).resolve().parent
        self.model_path = (
            base_path
            / "models"
            / "face_recognition_sface_2021dec.onnx"
        )

        self.data_folder = (
            base_path.parent.parent
            / "data"
            / "faces"
        )

        self.data_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.embedding_file = (
            self.data_folder / "amol.npy"
        )

        self.recognizer = None

        try:

            if not self.model_path.exists():
                print(
                    "[Face Recognition] "
                    "SFace model not found."
                )
                return

            self.recognizer = cv2.FaceRecognizerSF.create(
                str(self.model_path),
                ""
            )

            self.available = True

            if self.embedding_file.exists():

                self.enrolled = True
                self.authorized_user = "amol"

                print(
                    "[Face Recognition] "
                    "Authorized face loaded."
                )

        except Exception as exc:

            print(
                "[Face Recognition] "
                f"Initialization error: {exc}"
            )

    def is_available(self):

        return (
            self.available
            and self.recognizer is not None
        )

    def _extract_embedding(self, frame, face):

        if not self.is_available():
            return None

        try:

            aligned_face = self.recognizer.alignCrop(
                frame,
                face
            )

            feature = self.recognizer.feature(
                aligned_face
            )

            return feature

        except Exception as exc:

            print(
                "[Face Recognition] "
                f"Feature error: {exc}"
            )

            return None

    def enroll_face(
        self,
        frame,
        face,
        user_id="amol"
    ):

        if not self.is_available():
            return False

        if not user_id:
            return False

        feature = self._extract_embedding(
            frame,
            face
        )

        if feature is None:
            return False

        try:

            user_id = user_id.strip().lower()

            np.save(
                self.embedding_file,
                feature
            )

            self.authorized_user = user_id
            self.enrolled = True

            print(
                "[Face Recognition] "
                f"Face enrolled for {user_id}."
            )

            return True

        except Exception as exc:

            print(
                "[Face Recognition] "
                f"Enrollment error: {exc}"
            )

            return False

    def recognize_face(
        self,
        frame,
        face
    ):

        if not self.is_available():

            return {
                "recognized": False,
                "user": None,
                "reason": (
                    "Face recognition system "
                    "is unavailable."
                )
            }

        if not self.embedding_file.exists():

            self.enrolled = False

            return {
                "recognized": False,
                "user": None,
                "reason": (
                    "No authorized face is enrolled."
                )
            }

        feature = self._extract_embedding(
            frame,
            face
        )

        if feature is None:

            return {
                "recognized": False,
                "user": None,
                "reason": (
                    "Unable to extract face features."
                )
            }

        try:

            reference = np.load(
                self.embedding_file
            )

            score = self.recognizer.match(
                feature,
                reference,
                cv2.FaceRecognizerSF_FR_COSINE
            )

            threshold = 0.363

            if score >= threshold:

                self.authorized_user = "amol"
                self.enrolled = True

                return {
                    "recognized": True,
                    "user": "amol",
                    "reason": (
                        f"Face recognized. "
                        f"Similarity: {score:.3f}"
                    )
                }

            return {
                "recognized": False,
                "user": None,
                "reason": (
                    f"Face not recognized. "
                    f"Similarity: {score:.3f}"
                )
            }

        except Exception as exc:

            return {
                "recognized": False,
                "user": None,
                "reason": (
                    f"Recognition error: {exc}"
                )
            }

    def reset(self):

        self.authorized_user = None
        self.enrolled = False

    def get_status(self):

        return {
            "enrolled": self.enrolled,
            "user": self.authorized_user,
            "available": self.available,
            "embedding": str(
                self.embedding_file
            )
        }