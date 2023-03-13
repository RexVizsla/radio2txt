import time
import os
import datetime

dir_path = "/root/whisper/empty"

while True:
    for filename in os.listdir(dir_path):
        now = datetime.datetime.now()
        threshold = now - datetime.timedelta(hours=4)
        file_path = os.path.join(dir_path, filename)
        # Check if the file is older than the threshold time
        if os.path.isfile(file_path) and os.path.getmtime(file_path) < threshold.timestamp():
            # Delete the file
            os.remove(file_path)
            print(f"Deleted {filename}")
    print(f"Check done at {now}. Repeating in 30 minutes.")
    time.sleep(1800)