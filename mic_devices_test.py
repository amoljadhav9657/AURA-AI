import pyaudio

p = pyaudio.PyAudio()

for i in [1, 5, 9, 10]:

    try:
        info = p.get_device_info_by_index(i)

        print("")
        print("=" * 50)
        print("DEVICE:", i)
        print("NAME:", info["name"])
        print("INPUT CHANNELS:", info["maxInputChannels"])
        print("DEFAULT RATE:", info["defaultSampleRate"])

        if info["maxInputChannels"] <= 0:
            print("❌ NOT AN INPUT DEVICE")
            continue

        rate = int(info["defaultSampleRate"])

        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            input_device_index=i,
            frames_per_buffer=1024
        )

        print("✅ STREAM OPENED")

        data = stream.read(
            1024,
            exception_on_overflow=False
        )

        print("✅ AUDIO DATA:", len(data), "bytes")

        stream.stop_stream()
        stream.close()

    except Exception as exc:
        print("❌ FAILED:", type(exc).__name__, ":", exc)

p.terminate()
