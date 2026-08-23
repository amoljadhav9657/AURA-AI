import speech_recognition as sr

r = sr.Recognizer()

print("=" * 50)
print("AURA AI - SAVED WAV GOOGLE TEST")
print("=" * 50)

with sr.AudioFile("aura_test_audio.wav") as source:
    print("Loading WAV...")
    audio = r.record(source)

print("Audio loaded.")
print("Sending WAV to Google...")

try:
    result = r.recognize_google(
        audio,
        language="en-IN"
    )

    print("")
    print("✅ RESULT:", result)

except sr.UnknownValueError:
    print("❌ Google could not understand the saved WAV.")

except sr.RequestError as exc:
    print("❌ Google API error:", exc)

except Exception as exc:
    print("❌ ERROR:", type(exc).__name__, ":", exc)
