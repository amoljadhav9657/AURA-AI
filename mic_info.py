import pyaudio

p = pyaudio.PyAudio()

for i in [1, 5, 9]:
    info = p.get_device_info_by_index(i)

    print("")
    print("=" * 50)
    print("DEVICE:", i)
    print("NAME:", info["name"])
    print("INPUT:", info["maxInputChannels"])
    print("RATE:", info["defaultSampleRate"])

p.terminate()
