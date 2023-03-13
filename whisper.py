import os
import re
from datetime import datetime, timedelta
import time
import whisper
import shutil

queue_path = "/root/whisper/queue"
results_path = "/root/whisper/results.txt"
processed_folder = "/root/whisper/processed"

model = whisper.load_model("tiny")

while True:
    queue_files = os.listdir(queue_path)
    if not queue_files:
        print("No files found in queue...")
        time.sleep(1)
        continue
    dates = [datetime.strptime(filename.split('.')[0], '%Y-%m-%d_%H-%M-%S') for filename in queue_files]
    earliest_date = min(dates)
    earliest_file = f'{earliest_date.strftime("%Y-%m-%d_%H-%M-%S")}.wav'
    print(f"Starting transcription of {earliest_file}.")
    res = model.transcribe(f"{queue_path}/{earliest_file}", fp16=False, language="German")
    while True:
        try:
            shutil.move(f"{queue_path}/{earliest_file}", processed_folder)
            break
        except Exception():
            print("Cant move file to processed folder, retrying...")
            time.sleep(1)
            continue
    print("Transcription result: " + res["text"])
    if res["text"] != "\n":
        with open(results_path, "w") as f:
            f.write("\n" + earliest_date.strftime("%Y-%m-%d %H:%M:%S") + ": " + res["text"])