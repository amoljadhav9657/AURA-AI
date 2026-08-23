import cv2

from src.face.face_auth import FaceAuthManager


auth = FaceAuthManager()

print("=" * 60)
print("AURA AI - FACE ENROLLMENT")
print("=" * 60)

if not auth.is_available():
    print("❌ Face authentication system unavailable.")
    raise SystemExit(1)

print("📷 Camera starting...")
print("👤 Look directly at the camera.")
print("⏳ Keep your face steady...")

result = auth.enroll("amol")

print("\nEnrollment Result:")
print(result)

if result.get("success"):
    print("\n✅ FACE ENROLLMENT SUCCESSFUL")
    print("User: amol")
else:
    print("\n❌ FACE ENROLLMENT FAILED")
    print("Reason:", result.get("reason"))