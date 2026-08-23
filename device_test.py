import speech_recognition as sr

print("AURA MICROPHONE DEVICE TEST")
print("=" * 40)

for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(i, "->", name)

print("")
print("Testing device 10...")

try:
    mic = sr.Microphone(device_index=10)

    with mic as source:
        print("✅ DEVICE 10 OPENED")
        print("Sample rate:", source.SAMPLE_RATE)
        print("Chunk size:", source.CHUNK)

except Exception as exc:
    print("❌ DEVICE 10 FAILED")
    print(type(exc).__name__, ":", exc)
