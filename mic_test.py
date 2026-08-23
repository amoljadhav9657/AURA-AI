import speech_recognition as sr

r = sr.Recognizer()

print("========================================")
print("AURA AI MICROPHONE TEST")
print("========================================")
print("Device: 10 - Microphone Array")
print("Calibrating background noise...")

with sr.Microphone(device_index=10) as source:

    r.adjust_for_ambient_noise(source, duration=2)

    print("Energy threshold:", r.energy_threshold)
    print("")
    print("🎤 SPEAK NOW: HELLO AURA")

    audio = r.listen(
        source,
        timeout=10,
        phrase_time_limit=6
    )

print("Recognizing...")

try:
    text = r.recognize_google(audio)
    print("RESULT:", text)

except sr.UnknownValueError:
    print("❌ Could not understand audio.")

except sr.RequestError as exc:
    print("❌ Google Speech Recognition error:", exc)

except Exception as exc:
    print("❌ Error:", exc)
