import wave
import numpy as np
import shutil
import os
from datetime import datetime, timedelta
import time

received = "/root/whisper/received"
empty_folder = "/root/whisper/empty"
queue_folder = "/root/whisper/queue"

while True:
    for filename in os.listdir(received):
        wav_path = os.path.join(received, filename)
        mod_time = datetime.fromtimestamp(os.path.getmtime(wav_path))
        time_diff = datetime.now() - mod_time
        if time_diff < timedelta(seconds=10):
            continue
        try:
            # Open the wav file
            with wave.open(wav_path, 'r') as wav_file:
                # Get the number of frames in the audio signal
                n_frames = wav_file.getnframes()
                # Read all frames from the audio signal
                frames = wav_file.readframes(n_frames)
                # Ensure that frames is a multiple of 2 (for int16 dtype)
                frames += b'\x00' * (len(frames) % 2)
                # Convert the frames to a numpy array
                audio = np.frombuffer(frames, dtype=np.int16)
                # Calculate the root-mean-square (RMS) amplitude of the audio signal
                rms_amp = np.sqrt(np.mean(audio**2))
                if rms_amp < 1:
                    while True:
                        try:
                            shutil.move(wav_path, empty_folder)
                            print(f"Moved {filename} to {empty_folder}.")
                            break
                        except Exception:
                            print("Can't move file to empty folder, retrying...")
                            time.sleep(2)
                            continue
                else:
                    while True:
                        try:
                            shutil.move(wav_path, queue_folder)
                            print(f"Moved {filename} to {queue_folder}.")
                            break
                        except Exception:
                            print("Can't move file to queue folder, retrying...")
                            time.sleep(2)
                            continue
        except Exception:
            print("Can't read file: {}".format(filename))
    time.sleep(2)
