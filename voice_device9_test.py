import speech_recognition as sr

r = sr.Recognizer()

r.energy_threshold = 300
r.dynamic_energy_threshold = True
r.pause_threshold = 0.8
r.phrase_threshold = 0.3
r.non_speaking_duration = 0.5

print("=" * 50)
print("AURA AI - DEVICE 9 VOICE TEST")
print("=" * 50)

try:

    with sr.Microphone(device_index=9) as source:

        print("Calibrating background noise...")
        r.adjust_for_ambient_noise(source, duration=2)

        print("Energy threshold:", r.energy_threshold)
        print("")
        print("🎤 SPEAK: HELLO AURA")
        print("")

        audio = r.listen(
            source,
            timeout=10,
            phrase_time_limit=6
        )

    print("Recognizing...")

    text = r.recognize_google(audio)

    print("")
    print("✅ RESULT:", text)

except sr.WaitTimeoutError:
    print("❌ No speech detected.")

except sr.UnknownValueError:
    print("❌ Speech detected, but could not understand it.")

except sr.RequestError as exc:
    print("❌ Google recognition error:", exc)

except Exception as exc:
    print("❌ ERROR:", type(exc).__name__, ":", exc)
