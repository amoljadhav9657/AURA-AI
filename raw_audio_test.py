import speech_recognition as sr
import wave

r = sr.Recognizer()

print("=" * 50)
print("AURA AI - RAW AUDIO TEST")
print("=" * 50)

with sr.Microphone(device_index=9) as source:

    r.adjust_for_ambient_noise(source, duration=1)

    print("Energy threshold:", r.energy_threshold)
    print("")
    print("🎤 SPEAK CLEARLY: HELLO AURA")
    print("Recording for 5 seconds...")

    audio = r.record(source, duration=5)

print("✅ Recording completed")
print("Audio bytes:", len(audio.frame_data))

with open("aura_test_audio.wav", "wb") as f:
    f.write(audio.get_wav_data())

print("✅ Saved: aura_test_audio.wav")
