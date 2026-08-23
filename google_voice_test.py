import speech_recognition as sr
import time

r = sr.Recognizer()

print("=" * 50)
print("AURA AI - GOOGLE SPEECH TEST")
print("=" * 50)

with sr.Microphone(device_index=9) as source:

    print("Calibrating...")
    r.adjust_for_ambient_noise(source, duration=1)

    # Background noise मुळे threshold खूप वाढू नये
    r.energy_threshold = max(300, min(r.energy_threshold, 700))

    print("Energy threshold:", r.energy_threshold)
    print("")
    print("🎤 SPEAK NOW: HELLO AURA")

    audio = r.listen(
        source,
        timeout=10,
        phrase_time_limit=5
    )

print("Audio captured.")
print("Sending to Google...")
print("")

start = time.time()

try:

    text = r.recognize_google(
        audio,
        language="en-IN"
    )

    elapsed = time.time() - start

    print("✅ RESULT:", text)
    print(f"⏱️ Recognition time: {elapsed:.2f} seconds")

except sr.UnknownValueError:

    print("❌ Google could not understand the audio.")

except sr.RequestError as exc:

    print("❌ Google Speech API error:")
    print(exc)

except Exception as exc:

    print("❌ ERROR:")
    print(type(exc).__name__, ":", exc)
