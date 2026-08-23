import pyaudio
import speech_recognition as sr

device_index = 10

p = pyaudio.PyAudio()

info = p.get_device_info_by_index(device_index)

print("DEVICE:", device_index)
print("NAME:", info["name"])
print("INPUT CHANNELS:", info["maxInputChannels"])
print("DEFAULT RATE:", info["defaultSampleRate"])

try:
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=48000,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=1024
    )

    print("✅ PYAudio stream OPENED")

    data = stream.read(
        1024,
        exception_on_overflow=False
    )

    print("✅ AUDIO DATA RECEIVED:", len(data), "bytes")

    stream.stop_stream()
    stream.close()

except Exception as exc:
    print("❌ AUDIO STREAM FAILED")
    print(type(exc).__name__, ":", exc)

finally:
    p.terminate()
