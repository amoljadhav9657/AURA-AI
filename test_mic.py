import speech_recognition as sr

DEVICE = 1

r = sr.Recognizer()

print("=" * 50)
print("AURA AI - MICROPHONE TEST")
print("=" * 50)
print("Testing DEVICE:", DEVICE)
print("")
print("🎤 5 seconds recording सुरू होईल.")
print("या वेळेत स्पष्टपणे बोला:")
print("HELLO AURA, THIS IS AMOL")
print("")

with sr.Microphone(device_index=DEVICE) as source:

    print("Recording...")
    audio = r.record(source, duration=5)

print("✅ Recording completed")
print("Audio bytes:", len(audio.frame_data))

filename = f"device_{DEVICE}_test.wav"

with open(filename, "wb") as f:
    f.write(audio.get_wav_data())

print("✅ Saved:", filename)
print("")
print("Play the file and check whether YOUR voice is clear.")
