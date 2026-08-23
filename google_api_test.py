import speech_recognition as sr
import socket
import time

print("=" * 50)
print("AURA AI - SPEECH API CONNECTION TEST")
print("=" * 50)

print("Testing Google DNS/connection...")

try:
    socket.create_connection(("www.google.com", 443), timeout=5)
    print("✅ Google HTTPS connection available")
except Exception as exc:
    print("❌ Google HTTPS connection failed:", exc)
    raise SystemExit

r = sr.Recognizer()

try:

    with sr.Microphone(device_index=9) as source:

        print("Calibrating...")
        r.adjust_for_ambient_noise(source, duration=1)

        r.energy_threshold = 500

        print("Energy threshold:", r.energy_threshold)
        print("")
        print("🎤 SPEAK NOW: HELLO AURA")

        audio = r.listen(
            source,
            timeout=10,
            phrase_time_limit=5
        )

    print("✅ Audio captured")
    print("Audio bytes:", len(audio.frame_data))
    print("")
    print("Calling Google Speech Recognition...")
    print("⏳ Waiting maximum 15 seconds...")

    start = time.time()

    # Run recognition
    text = r.recognize_google(
        audio,
        language="en-IN"
    )

    elapsed = time.time() - start

    print("")
    print("✅ RESULT:", text)
    print("Recognition time:", round(elapsed, 2), "seconds")

except sr.UnknownValueError:
    print("❌ Google received audio but could not understand it.")

except sr.RequestError as exc:
    print("❌ Google Speech Recognition RequestError:")
    print(exc)

except Exception as exc:
    print("❌ ERROR:", type(exc).__name__, ":", exc)
