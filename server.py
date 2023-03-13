import subprocess
import requests
import time
import datetime
import os
import socket
import wave
import pyaudio
import threading

upload_ip = "192.168.178.63"
upload_port = 4455
chunk_size = 1024
record_length = 30
output_dir = r"C:\Users\rexvizsla\Documents\Busfunk_temp"
finished_file_path = None
last_uploaded = None

print(f"The file will be saved to {output_dir} and will be uploaded to {upload_ip} on port {upload_port}.")
print(f"Please continue to SDRUno and set all parameters.\nPress enter to continue.\n")
input()

def record():
    global finished_file_path
    while True:
        current_time = datetime.datetime.now()
        file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.wav")
        file_path = os.path.join(output_dir, file_name)
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=32000,
                            input=True,
                            frames_per_buffer=512)
        frames = []
        for i in range(0, int(32000 / 512 * record_length)):
            data = stream.read(512)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        wave_file = wave.open(file_path, "wb")
        wave_file.setnchannels(1)
        wave_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(32000)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        finished_file_path = file_path


def upload():
    global finished_file_path
    global last_uploaded
    while True:
        time.sleep(1)
        if finished_file_path != last_uploaded:
            while True:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((upload_ip, upload_port))
                    with open(finished_file_path, "rb") as f:
                        while True:
                            data = f.read(chunk_size)
                            if not data:
                                break
                            sock.send(data)
                    current_time = (datetime.datetime.now()).strftime("%H:%M:%S")
                    print(f"File {finished_file_path} uploaded successfully at {current_time}.")
                    sock.close()
                    last_uploaded = finished_file_path
                    break
                except Exception as e:
                    current_time = (datetime.datetime.now()).strftime("%H:%M:%S")
                    print(f"File {finished_file_path} upload failed at {current_time}: {e}")
                    time.sleep(2)
                    continue
        else:
            continue

record_thread = threading.Thread(target=record)
upload_thread = threading.Thread(target=upload)
record_thread.start()
upload_thread.start()