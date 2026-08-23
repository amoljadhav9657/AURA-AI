import wave
import audioop

filename = "aura_test_audio.wav"

with wave.open(filename, "rb") as w:
    frames = w.readframes(w.getnframes())
    width = w.getsampwidth()
    channels = w.getnchannels()
    rate = w.getframerate()

rms = audioop.rms(frames, width)

print("=" * 50)
print("AURA AI - AUDIO LEVEL TEST")
print("=" * 50)
print("Sample rate :", rate)
print("Channels    :", channels)
print("Sample width:", width)
print("RMS level   :", rms)

if rms < 300:
    print("❌ VERY LOW AUDIO")
elif rms < 1000:
    print("⚠️ LOW AUDIO")
elif rms < 5000:
    print("✅ GOOD AUDIO LEVEL")
else:
    print("⚠️ VERY LOUD / NOISY AUDIO")
